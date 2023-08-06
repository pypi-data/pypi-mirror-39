# Copyright 2016-2018 Autodesk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import print_function, unicode_literals, absolute_import, division

import tempfile

import requests
from future import standard_library
standard_library.install_aliases()
from future.builtins import *

import os
import io
import tarfile

from . import CachedFile
from .. import exceptions


class _FetchFunction(object):
    """Convenience descriptor for methods that need to download a file before doing anything"""
    def __init__(self, funcname):
        self.funcname = funcname

    def __get__(self, instance, cls):
        instance.download()
        return getattr(super(LazyFetcherBase, instance), self.funcname)


class LazyFetcherBase(CachedFile):
    """
    A base class for for dealing with files that need to be downloaded - they are cached
    locally when downloaded.
    """
    REMOTE = True

    def __init__(self):
        self._fetched = False
        self.localpath = None

    def size_bytes(self):
        if self.localpath is not None:
            return super().size_bytes()
        else:
            raise NotImplementedError("Sizes only available for local files")

    put = _FetchFunction('put')
    open = _FetchFunction('open')
    read = _FetchFunction('read')
    readlines = _FetchFunction('readlines')
    __iter__ = _FetchFunction('__iter__')

    def download(self):
        if not self._fetched:
            self._fetch()
            self._fetched = True

    def _fetch(self):
        raise NotImplemented("_fetch needs to be implemented by subclass")

    def __str__(self):
        if self._fetched:
            return super(LazyFetcherBase, self).__str__()
        else:
            return 'Reference to %s (not downloaded)' % self.source


class HttpContainer(LazyFetcherBase):
    """
    Lazily fetched file on the web. Will cache it in CACHEDIR ('/tmp/cyborgcache')
    by default, then treat it as a CachedFile class

    Unlike other remote files, this one doesn't preserve the file contents when pickled;
    instead, we assume that it should still be accessible (not always a good assumption!)
    """
    def __reduce__(self):
        return self.__class__, (self.source,)

    def __init__(self, url):
        self.source = url
        self.sourcetype = 'HTTP request'
        super(HttpContainer, self).__init__()

    def _fetch(self):
        self._open_tmpfile()
        request = requests.get(self.source)
        self.tmpfile.write(request.content)
        self.tmpfile.close()
        self.localpath = self.tmpfile.name
        self._fetched = True


class LazyDockerCopy(LazyFetcherBase):
    """
    Lazily copies the file from the worker.
    This is, of course, problematic if the worker is not accessible from the client.
    """
    def __init__(self, dockerhost, containerid, containerpath):
        self.source = "%s (%s)://%s" % (dockerhost, containerid, containerpath)
        self.sourcetype = 'Docker container'
        self.dockerhost = dockerhost
        self.containerpath = containerpath
        self.containerid = containerid
        self.basename = os.path.basename(containerpath)
        super(LazyDockerCopy, self).__init__()

    def _fetch(self):
        import shutil

        # extracts the stream into a disk-spooled file-like object
        tarfile_path = os.path.basename(self.containerpath)
        stream = self._get_tarstream()
        try:
            with tempfile.SpooledTemporaryFile() as buffer:
                for d in stream:
                    buffer.write(d)
                buffer.seek(0)
                tar = tarfile.open(fileobj=buffer)
                filestream = tar.extractfile(tarfile_path)

                if filestream is None:
                    fileinfo = tar.getmember(tarfile_path)
                    if fileinfo.type == tarfile.DIRTYPE:
                        from future.utils import PY2
                        if PY2:
                            import errno
                            raise OSError(self, errno=errno.EISDIR)
                        else:
                            raise IsADirectoryError(self)

                    else:
                        raise exceptions.NotARegularFileError(self)

                self._open_tmpfile()
                try:
                    shutil.copyfileobj(filestream, self.tmpfile)
                finally:
                    self.tmpfile.close()

        finally:
            stream.close()

        self.localpath = self.tmpfile.name
        self._fetched = True

    def _get_tarstream(self):
        from .. import docker_utils as du
        client = du.get_docker_apiclient(**self.dockerhost)
        args = (self.containerid, self.containerpath)
        if hasattr(client, 'get_archive'):  # handle different docker-py versions
            request, meta = client.get_archive(*args)
        else:
            request = client.copy(*args)
        return request
