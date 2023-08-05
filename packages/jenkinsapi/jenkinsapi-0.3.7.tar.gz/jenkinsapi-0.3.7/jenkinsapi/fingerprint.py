"""
Module for jenkinsapi Fingerprint
"""

from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.custom_exceptions import ArtifactBroken

import re
import requests

import logging

log = logging.getLogger(__name__)


class Fingerprint(JenkinsBase):

    """
    Represents a jenkins fingerprint on a single artifact file ??
    """
    RE_MD5 = re.compile("^([0-9a-z]{32})$")

    def __init__(self, baseurl, id_, jenkins_obj):
        logging.basicConfig()
        self.jenkins_obj = jenkins_obj
        assert self.RE_MD5.search(id_), ("%s does not look like "
                                         "a valid id" % id_)
        url = "%s/fingerprint/%s/" % (baseurl, id_)
        JenkinsBase.__init__(self, url, poll=False)
        self.id_ = id_
        self.unknown = False  # Previously uninitialized in ctor

    def get_jenkins_obj(self):
        return self.jenkins_obj

    def __str__(self):
        return self.id_

    def valid(self):
        """
        Return True / False if valid. If returns True, self.unknown is
        set to either True or False, and can be checked if we have
        positive validity (fingerprint known at server) or negative
        validity (fingerprint not known at server, but not really an
        error).
        """
        try:
            self.poll()
            self.unknown = False
        except requests.exceptions.HTTPError as err:
            # We can't really say anything about the validity of
            # fingerprints not found -- but the artifact can still
            # exist, so it is not possible to definitely say they are
            # valid or not.
            # The response object is of type: requests.models.Response
            # extract the status code from it
            response_obj = err.response
            if response_obj.status_code == 404:
                logging.warning(
                    "MD5 cannot be checked if fingerprints are not "
                    "enabled")
                self.unknown = True
                return True

            return False

        return True

    def validate_for_build(self, filename, job, build):
        if not self.valid():
            log.info("Unknown to jenkins.")
            return False
        if self.unknown:
            # not request error, but unknown to jenkins
            return True
        if self._data["original"] is not None:
            if self._data["original"]["name"] == job:
                if self._data["original"]["number"] == build:
                    return True
        if self._data["fileName"] != filename:
            log.info(
                msg="Filename from jenkins (%s) did not match provided (%s)" %
                (self._data["fileName"], filename))
            return False
        for usage_item in self._data["usage"]:
            if usage_item["name"] == job:
                for range_ in usage_item["ranges"]["ranges"]:
                    if range_["start"] <= build <= range_["end"]:
                        msg = ("This artifact was generated by %s "
                               "between build %i and %i" %
                               (job, range_["start"], range_["end"]))
                        log.info(msg=msg)
                        return True
        return False

    def validate(self):
        try:
            assert self.valid()
        except AssertionError:
            raise ArtifactBroken(
                "Artifact %s seems to be broken, check %s" %
                (self.id_, self.baseurl))
        except requests.exceptions.HTTPError:
            raise ArtifactBroken(
                "Unable to validate artifact id %s using %s" %
                (self.id_, self.baseurl))
        return True

    def get_info(self):
        """
        Returns a tuple of build-name, build# and artifact filename
        for a good build.
        """
        self.poll()
        return self._data["original"]["name"], \
            self._data["original"]["number"], self._data["fileName"]
