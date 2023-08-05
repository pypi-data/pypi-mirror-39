# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python imports
import os
import zipfile

# Django imports
from django import http
from django.db import models
from django.views import generic

# Devilry/cradmin imports
from django_cradmin import crapp
from devilry.devilry_group import models as group_models
from devilry.devilry_comment.models import CommentFile
from devilry.devilry_group.models import GroupComment, ImageAnnotationComment


class ZipBuffer(object):
    """ A file-like object for zipfile.ZipFile to write into. """

    def __init__(self):
        self.data = []
        self.pos = 0

    def write(self, data):
        self.data.append(data)
        self.pos += len(data)

    def tell(self):
        # zipfile calls this so we need it
        return self.pos

    def flush(self):
        # zipfile calls this so we need it
        pass

    def get_and_clear(self):
        result = self.data
        self.data = []
        return result


class BulkFileDownloadBaseView(generic.View):
    def get_queryset(self, request):
        raise NotImplementedError("get_queryset() must be implemented by subclass!")

    def get_zipfilename(self, request):
        raise NotImplementedError("get_zipfilename() must be implemented by subclass!")

    def __get_rootlabel(self, feedbackset):
        """
        Builds and returns the rootlevel of a filename in a zip-archive

        :param feedbackset:
            The current FeedbackSet being iterated over by get_filestructure()
        :return:
            A string like: "duck1010.spring2015.oblig1.donald.dolly/"
        """
        return "{}.{}.{}.{}/".format(
                feedbackset.group.assignment.period.subject.short_name,
                feedbackset.group.assignment.period.short_name,
                feedbackset.group.assignment.short_name,
                ".".join(feedbackset.group.short_displayname.split(', ')))

    def __get_attemptlabel(self, feedbackset, attemptcounter):
        """
        Calculates what deliveryattempt the current FeedbackSet is, and returns the correct label for use
        in filepath in zip-archive

        :param feedbackset:
            The current FeedbackSet being iterated over by get_filestructure()
        :param attemptcounter:
            The attemptnumber for the previously iterated FeedbackSet
        :return:
            New attemptcounter and a label like: "attempt1/"
        """
        if feedbackset.feedbackset_type == feedbackset.FEEDBACKSET_TYPE_FIRST_ATTEMPT:
            attemptcounter = 1
        elif feedbackset.feedbackset_type == feedbackset.FEEDBACKSET_TYPE_NEW_ATTEMPT:
            attemptcounter += 1
        return attemptcounter, "attempt{}/".format(attemptcounter)

    def __check_if_subfolder(self, feedbackset, commentfile):
        """
        check if user is examiner, if so, return the label "from_examiner/"
        if user is student, and comment was created after deadline, return label "not_part_of_delivery/".
        :param commentfile:
            The current commentfile being iterated over in get_filestructure()
        :param rootlabel:
            The rootlabel generated by __get_rootlabel()
        :param attemptlabel:
            The attemptlabel generated by __get_attemptlabel()
        :return:
            string "from_examiner/" if user is examiner,
             "not_part_of_delivery/" if user is student and posted after deadline,
             empty string if neither of the above..

        :return:
            None if user is not student or examiner (this commentfile will then be ignored for zip..)
        """
        if commentfile.comment.user_role == commentfile.comment.USER_ROLE_STUDENT and \
                        commentfile.comment.created_datetime > feedbackset.deadline_datetime:
                return "not_part_of_delivery/"

        elif commentfile.comment.user_role == commentfile.comment.USER_ROLE_EXAMINER:
            return "from_examiner/"

        return ""

    def __get_full_archivename(self, files, commentfile, archivebasename):
        """
        combine all current segments into one final filename for archive. Also handles identical filenames in same
        folder.

        :param files:
            All files already added
        :param commentfile:
            the commentfile currently being iterated over
        :param archivebasename:
            the basename returned by __check_if_examiner
        :return:
            full path and filename to add the current file to archive
        """
        identical_filenames_counter = 0
        split_filename = os.path.splitext(commentfile.filename)
        archivename = "{}{}".format(archivebasename, commentfile.filename)
        while archivename in files.keys():
            identical_filenames_counter += 1
            archivename = "{}{}-{}{}".format(archivebasename,
                                             split_filename[0],
                                             identical_filenames_counter,
                                             split_filename[1])
        return archivename

    def __optimize_queryset(self, queryset):
        commentfile_queryset = CommentFile.objects.order_by('created_datetime')
        groupcomment_queryset = GroupComment.objects\
            .order_by('created_datetime')\
            .prefetch_related(models.Prefetch('commentfile_set',
                                              queryset=commentfile_queryset))
        imageannotationcomment_queryset = ImageAnnotationComment.objects\
            .order_by('created_datetime')\
            .prefetch_related(models.Prefetch('commentfile_set',
                                              queryset=commentfile_queryset))
        return queryset\
            .order_by('group_id', 'created_datetime')\
            .prefetch_related(models.Prefetch('groupcomment_set',
                                              queryset=groupcomment_queryset))\
            .prefetch_related(models.Prefetch('imageannotationcomment_set',
                                              queryset=imageannotationcomment_queryset))

    def get_filestructure(self, queryset):
        """
        Iterate all FeedbackSet's in given queryset and build a dict containing archivepaths and actual filepaths
        for all commentfiles.

        Final result will allow for a zip-archive structure like this::

            inf2100.oblig2.student1.student2/
                - attempt1/
                    - not_part_of_delivery/
                        - otherstuff.java
                        - .....
                    - from_examiner
                        - otherstuff.java
                        - otherstuff-2.java
                        - .....
                    - somestuff.java
                    - .....
                - attempt2/
                    - .....
            inf2100.oblig2.student3.student4/
                - ....

        Args:
            queryset (QuerySet): The queryset to use.

        Returns:
            dict: Dictionary of :class:`~devilry.devilry_comment.models.CommentFile`s.
        """
        files = {}
        attemptcounter = 1
        for feedbackset in self.__optimize_queryset(queryset):
            rootlabel = self.__get_rootlabel(feedbackset)
            attemptcounter, attemptlabel = self.__get_attemptlabel(feedbackset, attemptcounter)
            for groupcomment in feedbackset.groupcomment_set.all():
                # TODO: Permission checks - only include what the user is allowed to see
                for commentfile in groupcomment.commentfile_set.all():
                    subfolderlabel = self.__check_if_subfolder(feedbackset, commentfile)
                    archivebasename = "{}{}{}".format(rootlabel, attemptlabel, subfolderlabel)
                    archivename = self.__get_full_archivename(files, commentfile, archivebasename)
                    files[archivename] = commentfile
            # TODO: Same thing as for groupcomment_set, but for imageannotationcomment_set

        return files

    def generate_zipped_stream(self, queryset):
        """
        Build a zip-archive with structure defined by get_filestructure() in memory using ZipBuffer, and yield chunks
        for streaming to response

        Args:
            queryset(QuerySet): The queryset to use.
        """
        sink = ZipBuffer()
        archive = zipfile.ZipFile(sink, "w")
        files = self.get_filestructure(queryset)
        for archivename, commentfile in files.iteritems():
            archive.writestr(archivename, commentfile.file.read())
            for chunk in sink.get_and_clear():
                yield chunk

        archive.close()
        # close() generates some more data, so we yield that too
        for chunk in sink.get_and_clear():
            yield chunk

    def get(self, request):
        """
        Generate a HttpResponse with a zipped collection of files.

        Args:
            request (HttpRequest): request for the view.

        Returns:
            HttpResponse: created response.
        """
        queryset = self.get_queryset(request)
        if not queryset.exists():
            return http.Http404()  # TODO: fitting errmsg
        response = http.HttpResponse(self.generate_zipped_stream(queryset), content_type="application/zip")
        response['Content-Disposition'] = "attachment; filename={}".format(self.get_zipfilename(request))
        return response


class FeedbackfeedBulkFileDownload(BulkFileDownloadBaseView):
    """
    View that implements :class:`~.BulkFileDownloadBaseView` for downloading all files
    for an :class:`~devilry.apps.core.models.AssignmentGroup`.
    """
    def get_queryset(self, request):
        return group_models.FeedbackSet.objects.filter(group=request.cradmin_role)

    def get_zipfilename(self, request):
        return 'deliveryfile.zip'


class App(crapp.App):
    appurls = [
        crapp.Url(
            r'^bulk-filedownload$',
            FeedbackfeedBulkFileDownload.as_view(),
            name='bulk-filedownload'),
    ]
