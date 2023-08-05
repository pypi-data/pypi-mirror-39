#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

import collections
from functools import wraps
import multiprocessing
import os
import shutil
import socket
import sys
from sys import excepthook as _excepthook
import tempfile
import threading
import warnings

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from pytest_localftpserver.helper_functions import arg_validator, \
    arg_validator_excepthook, pretty_logger

import pytest

if sys.platform.startswith('linux'):
    USE_PROCESS = True
else:
    USE_PROCESS = False


# uncomment the next line to log _option_validator for debugging
# import logging
# logging.basicConfig(filename='option_validator.log', level=logging.INFO)


class SimpleFTPServer(FTPServer):
    """
    Starts a simple FTP server on a random free port.

    https://github.com/Lukasa/requests-ftp/
    """

    def __init__(self, username, password, ftp_home=None, ftp_port=0):
        # Create temp directories for the anonymous and authenticated roots
        self._anon_root = tempfile.mkdtemp(prefix="anon_root_")
        if not ftp_home:
            self.temp_ftp_home = True
            self._ftp_home = tempfile.mkdtemp(prefix="ftp_home_")
        else:
            self.temp_ftp_home = False
            self._ftp_home = ftp_home
        self.username = username
        self.password = password
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.username, self.password, self.ftp_home,
                            perm='elradfmwM')
        authorizer.add_anonymous(self.anon_root)

        handler = FTPHandler
        handler.authorizer = authorizer
        # Create a socket on any free port
        self._ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ftp_socket.bind(('127.0.0.1', ftp_port))
        self._ftp_port = self._ftp_socket.getsockname()[1]

        # Create a new pyftpdlib server with the socket and handler we've
        # configured
        FTPServer.__init__(self, self._ftp_socket, handler)

    @property
    def anon_root(self):
        """
        Home directory for the anonymous user
        """
        return self._anon_root

    @property
    def ftp_home(self):
        """
        FTP home for the ftp_user
        """
        return self._ftp_home

    @property
    def ftp_port(self):
        """
        Port the server is running on
        """
        return self._ftp_port

    def __del__(self):
        self.stop()

    def stop(self):
        """
        Stops the server, closes all the open ports and deletes all temp files
        """
        self.close_all()
        self.clear_tmp_dirs()

    def clear_tmp_dirs(self):
        """
        Clears all temp files generated on the FTP server
        """
        shutil.rmtree(self.anon_root, ignore_errors=True)
        if self.temp_ftp_home:
            shutil.rmtree(self.ftp_home, ignore_errors=True)

    def reset_tmp_dirs(self):
        """
        Clears all temp files generated on the FTP server and
        recreates the base dirs on the server.
        This method is implemented to have more control over
        the session based ftp server.
        """
        self.clear_tmp_dirs()
        # checking if the folder still exists prevents an error
        # being raised by os.makedirs
        if not os.path.exists(self.anon_root):  # pragma: no branch
            os.makedirs(self.anon_root)
        if self.temp_ftp_home:  # pragma: no branch
            if not os.path.exists(self.ftp_home):  # pragma: no branch
                os.makedirs(self.ftp_home)


class BaseMPFTPServer(object):
    """
    Baseclass which holds the functionality of ftpserver.
    The derived classes are ThreadFTPServer and ProcessFTPServer, which
    (depending on the OS) are the classes of the ftpserver instance.
    """
    def __init__(self, username, password, ftp_home, ftp_port):
        """

        Parameters
        ----------
        username: str
            Name of the registered user.
        password: str
            Password of the registered user.
        ftp_home: str
            Local path to FTP home for the registered user.
        ftp_port: int
            Desired port for the server to listen to.
        """
        self._server = SimpleFTPServer(username, password,
                                       ftp_home, ftp_port)

    @property
    def username(self):
        """
        Name of the registered user.
        """
        return self._server.username

    @property
    def password(self):
        """
        Password of the registered user.
        """
        return self._server.password

    @property
    def server_port(self):
        """
        Port the server is running on.
        """
        return self._server.ftp_port

    @property
    def server_home(self):
        """
        Local path to FTP home for the registered user.
        """
        return self._server.ftp_home

    @property
    def anon_root(self):
        """
        Local path to FTP home for the anonymous user.
        """
        return self._server._anon_root

    def _option_validator(valid_var_overwrite=None,
                          strict_type_check=True,
                          dev_mode=False,
                          debug=False):
        """
        Development helperfunction to raise appropriate Error if a methods arg/kwarg
        is of wrong type or value.

        If a arg/kwarg isn't in the default values defined in `valid_var_list`,
        add it to `valid_var_list` or use the option `valid_var_overwrite`,
        if it varies just in that case.


        Parameters
        ----------
        valid_var_overwrite: dict, iterable of dicts: default None
            This is used if in a special case, an args/kwargs value/type varies
            from the one defines in `valid_var_list`

        strict_type_check: bool: default True
            Weather or not to use strict Type checking

        dev_mode: bool: default False
            Weather or not to give warning if arguments are missing `valid_var_list`

        Raises
        ------
        TypeError
            If any of the checked args/kwargs has a not supported type

        ValueError
            If any of the checked args/kwargs has a not supported value
        """
        def inner_decorator(f):
            """
            Parameters
            ----------
            f: function, method
            """
            # this is needed so Sphinx will find the proper docstrings and signatures
            @wraps(f)
            def wrapper(self, *args, **kwargs):
                valid_var_list = {
                    "style":
                        {"valid_values": ['rel_path', 'url'],
                         "valid_types": [str]},
                    "anon":
                        {"valid_types": [bool]},
                    "rel_file_path":
                        {"valid_types": [str]},
                    "read_mode":
                        {"valid_values": ['r', 'rb'],
                         "valid_types": [str]},
                    "overwrite":
                        {"valid_types": [bool]},
                    "return_paths":
                        {"valid_values": ['all', 'input', 'new'],
                         "valid_types": [str]},
                    "return_content":
                        {"valid_types": [bool]}
                    }
                # generate a named function args dict {"arg_name": "args_value"}
                # the name of the first argument needs to be skipped since it is always self
                func_locals = dict(**dict(zip(f.__code__.co_varnames[1:], args)))
                func_locals.update(kwargs)
                if debug:
                    heading = f.__name__.upper()
                    msg_line = []
                    for key in sorted(func_locals):
                        msg_line.append("'{}': {}".format(key, func_locals[key]))
                    msg = "\n".join(msg_line)
                    pretty_logger(heading, "FUNC_LOCALS\n"+msg+"\n\n")
                try:
                    sys.excepthook = _excepthook
                    arg_validator(func_locals, valid_var_list, valid_var_overwrite,
                                  strict_type_check=strict_type_check, dev_mode=dev_mode,
                                  implementation_func_name=f.__name__)
                except (ValueError, TypeError) as e:
                    sys.excepthook = arg_validator_excepthook
                    raise e

                return f(self, *args, **kwargs)
            return wrapper

        return inner_decorator

    @_option_validator(debug=True)
    def __test_option_validator_logging__(self, a, b=3):
        """
        This method is only implemented for the purpose
        of testing the logging output of _option_validator.
        Since decorators aren't inherited testing of that behaviour
        would else be more complicated

        Parameters
        ----------
        a: any
        b: any, default 3
        """
        pass

    def reset_tmp_dirs(self):
        """
        Clears all temp files generated on the FTP server.
        This method is implemented to have more control over
        the module scoped ftp server.

        Examples
        --------

        filesystem before:

        .. code::

          filesystem
          +---server_home
          |   +---test_file1
          |   +---test_folder
          |       +---test_file2
          |
          +---anon_root
              +---test_file3
              +---test_folder
                  +---test_file4

        >>> ftpserver.reset_tmp_dirs()

        filesystem after:

        .. code::

          filesystem
          +---server_home
          |
          +---anon_root
        """
        self._server.reset_tmp_dirs()

    @_option_validator(
        valid_var_overwrite={
            "style":
                {"valid_values": ["dict", "url"],
                 'valid_types': [str]}
        })
    def get_login_data(self, style="dict", anon=False):
        """
        Returns the login data as dict or url.
        What the returned value looks like is depending on `style` and
        the anonymous user or registered user depending `anon`.

        Parameters
        ----------
        style: {'dict', 'url'}, default 'dict'
            'dict':
                returns a dict with keys `host`, `port`, `user`
                and `passwd` or only `host` and `port`

            'url':
                returns a url containing the the login data

        anon: bool
            True:
                returns the login data for the anonymous user

            False:
                returns the login data for the registered user

        Returns
        -------
        login_data: dict, str
            Login data as dict or url, depending on the value of `style`.

        Raises
        ------
        TypeError
            If `style` is not a ``str``
        TypeError
            If `anon` is not a ``bool``

        ValueError
            If the value of `style` is not 'dict' or 'url'

        Examples
        --------

        >>> ftpserver.get_login_data()
        {"host": "localhost", "port": 8888, "user": "fakeusername",
        "passwd": "qweqwe"}

        >>> ftpserver.get_login_data(anon=True)
        {"host": "localhost", "port": 8888}

        >>> ftpserver.get_login_data(style="url")
        ftp://fakeusername:qweqwe@localhost:8888

        >>> ftpserver.get_login_data(style="url", anon=True)
        ftp://localhost:8888

        """
        if style == "dict":
            login_dict = {"host": "localhost", "port": self.server_port}
            if not anon:  # pragma: no branch
                login_dict["user"] = self.username
                login_dict["passwd"] = self.password
            return login_dict
        # even so only 'dict' and 'url' are supported values
        # here else is used for a better branch coverage
        else:
            host = "localhost:"+str(self.server_port)
            if anon:
                return "ftp://"+host
            else:
                return "ftp://"+self.username+":"+self.password+"@"+host

    @_option_validator()
    def format_file_path(self, rel_file_path, style="rel_path", anon=False):
        """
        Formats the relative path to as relative path or url.
        Relative paths are relative to the server_home/anon_root, which can be used by a
        FTP client.
        Urls can be used by a browser/downloader.
        This method works, weather the file exists or not.

        Notes
        -----
        Even so taking a relative path and returning a relative path may
        seam pointless, this is needed to prevent errors with Windows path
        formatting (``\\`` instead of ``/``).

        Parameters
        ----------
        rel_file_path: str
            Relative filepath to server_home/anon_root depending on the value of anon.

        style: {'rel_path', 'url'}, default 'rel_path'
            'rel_path':
                path relative to server_home/anon_root is returned.

            'url':
                url to the file is returned.

        anon: bool
            True:
                return the filepaths/url of file in anon_root

            False:
                return the filepaths/url of file in server_home

        Returns
        -------
        file_path: str
            Relative path or url depending on the value of style

        Raises
        ------
        TypeError
            If `style` is not a ``str``
        TypeError
            If `anon` is not a ``bool``

        ValueError
            If the value of `style` is not 'rel_path' or 'url'

        Examples
        --------

        >>> ftpserver.format_file_path("test_folder\\test_file", style="rel_path", anon=False))
        test_folder/test_file

        >>> ftpserver.format_file_path("test_folder/test_file", style="rel_path", anon=False))
        test_folder/test_file

        >>> ftpserver.format_file_path("test_folder/test_file", style="url", anon=False))
        ftp://fakeusername:qweqwe@localhost:8888/test_folder/test_file

        >>> ftpserver.format_file_path("test_folder/test_file", style="url", anon=True))
        ftp://localhost:8888/test_folder/test_file

        See Also
        --------
        get_local_base_path
        get_file_paths

        """
        # the replace is needed for windows systems
        rel_file_path = rel_file_path.replace("\\", "/")
        if style == "rel_path":
            return rel_file_path
        # even so only 'rel_path' and 'url' are supported values
        # here else is used for a better branch coverage
        else:
            base_url = self.get_login_data(style="url", anon=anon)
            return base_url + "/" + rel_file_path

    @_option_validator()
    def get_local_base_path(self, anon=False):
        """
        Returns the basepath on the local file system.
        Depending on anon the basepath is for the registered
        or anonymous user.

        Parameters
        ----------
        anon: bool, default False

        anon: bool
            True:
                returns the local path to anon_root

            False:
                returns the local path to server_home

        Returns
        -------
        base_path: str
            Basepath on the local file system.

        Raises
        ------
        TypeError
            If `anon` is not a ``bool``

        Examples
        --------

        >>> ftpserver.get_local_base_path(anon=False))
        /tmp/ftp_home_1rg7_i

        >>> ftpserver.get_local_base_path(anon=True))
        /tmp/anon_root_m6fknmyx
        """
        if anon:
            base_path = self.anon_root
        else:
            base_path = self.server_home
        return base_path

    @_option_validator()
    def get_file_paths(self, style="rel_path", anon=False):
        """
        Yields the paths of all files server_home/anon_root, in the given `style`.

        Parameters
        ----------
        style: {'rel_path', 'url'}, default 'rel_path'
            'rel_path':
                path relative to server_home/anon_root is returned.

            'url':
                url to the file is returned.

        anon: bool
            True:
                filepaths/urls of all files in anon_root is returned.

            False:
                filepaths/urls of all files in server_home is returned.

        Yields
        ------
        file_path: str
            Generator of all filepaths in the server_home/anon_root

        Raises
        ------
        TypeError
            If `style` is not a ``str``
        TypeError
            If `anon` is not a ``bool``

        ValueError
            If the value of `style` is not 'rel_path' or 'url'

        Examples
        --------

        Assuming a file structure as follows.

        .. code::

          filesystem
          +---server_home
          |   +---test_file1
          |   +---test_folder
          |       +---test_file2
          |
          +---anon_root
              +---test_file3
              +---test_folder
                  +---test_file4


        >>> list(ftpserver.get_file_paths(style="rel_path", anon=False))
        ["test_file1", "test_folder/test_file2"]

        >>> list(ftpserver.get_file_paths(style="rel_path", anon=True))
        ["test_file3", "test_folder/test_file4"]



        >>> list(ftpserver.get_file_paths(style="url", anon=False))
        ["ftp://fakeusername:qweqwe@localhost:8888/test_file1",
        "ftp://fakeusername:qweqwe@localhost:8888/test_folder/test_file2"]

        >>> list(ftpserver.get_file_paths(style="url", anon=True))
        ["ftp://localhost:8888/test_file3", "ftp://localhost:8888/test_folder/test_file4"]

        """
        base_path = self.get_local_base_path(anon=anon)
        for root, dirs, files in os.walk(base_path):
            for file in files:
                rel_file_path = os.path.relpath(os.path.join(root, file),
                                                base_path)
                yield self.format_file_path(rel_file_path, style, anon)

    @_option_validator(
        valid_var_overwrite={
            "rel_file_paths":
                {'valid_types': [type(None),
                                 str,
                                 collections.Iterable]}
        },
        strict_type_check=False)
    # if you use dev_mode=True here you will get a warning that `rel_file_paths`, isn't in
    # `valid_var_list` this is on purpose, since `rel_file_paths` gets checked with
    # `strict_type_check=False` to be able to check `collections.Iterable`
    @_option_validator(dev_mode=False)
    def get_file_contents(self, rel_file_paths=None, style="rel_path",
                          anon=False, read_mode="r"):
        """
        Yields dicts containing the `path` and `content` of files on the FTP server.

        Parameters
        ----------
        rel_file_paths: str, list of str, None, default None
            None:
                The content of all files on the server will be retrieved.

            str or list of str:
                only the content of those files will be retrieved.

        style: {'rel_path', 'url'}, default 'rel_path'
            'rel_path':
                path relative to server_home/anon_root is returned.

            'url':
                A url to the file is returned.

        anon: bool
            True:
                return the filepaths/url of files in anon_root

            False:
                return the filepaths/url of files in in server_home

        read_mode: {'r', 'rb'}, default 'r'
            Mode in which files should be read (see ``open("filepath", read_mode)`` )

        Yields
        ------
        content_dict: dict
            Dict containing the file `path` as relpath or url (see `style`) and
            the `content` of the file as string or bytes (see `read_mode`)

        Raises
        ------
        TypeError
            If `rel_file_paths` is not ``None``, a ``str`` or an ``iterable``
        TypeError
            If `style` is not a ``str``
        TypeError
            If `anon` is not a ``bool``
        TypeError
            If `read_mode` is not a ``str``

        ValueError
            If the value of `rel_file_paths` or its items are not valid filepaths
        ValueError
            If the value of `style` is not 'rel_path' or 'url'
        ValueError
            If the value of `read_mode` is not 'r' or 'rb'

        Examples
        --------

        Assuming a file structure as follows.

        .. code::

          filesystem
          +---server_home
              +---test_file1.txt
              +---test_folder
                  +---test_file2.zip


        >>> list(ftpserver.get_file_contents())
        [{"path": "test_file1.txt", "content": "test text"},
         {"path": "test_folder/test_file2.txt", "content": "test text2"}]

        >>> list(ftpserver.get_file_contents("test_file1.txt"))
        [{"path": "test_file1.txt", "content": "test text"}]

        >>> list(ftpserver.get_file_contents("test_file1.txt", style="url"))
        [{"path": "ftp://fakeusername:qweqwe@localhost:8888/test_file1.txt",
          "content": "test text"}]

        >>> list(ftpserver.get_file_contents(["test_file1.txt", "test_folder/test_file2.zip"],
        ...                                  read_mode="rb"))
        [{"path": "test_file1.txt", "content": b"test text"},
         {"path": "test_folder/test_file2.zip", "content": b'PK\\x03\\x04\\x14\\x00\\x00...'}]


        See Also
        --------
        get_file_paths
        put_files
        """
        base_path = self.get_local_base_path(anon=anon)
        if not rel_file_paths:
            rel_file_paths = self.get_file_paths(style=style, anon=anon)
        if isinstance(rel_file_paths, str) or not isinstance(rel_file_paths, collections.Iterable):
            rel_file_paths = [rel_file_paths]
        for rel_file_path in rel_file_paths:
            if "ftp://" in rel_file_path:
                base_url = self.get_login_data(style="url", anon=anon)
                rel_file_path = os.path.relpath(rel_file_path, base_url)
            # the os.path.abspath is so windows doesn't mess up with \\ in paths
            abs_path = os.path.abspath(os.path.join(base_path, rel_file_path))
            if os.path.isfile(abs_path):
                rel_file_path = self.format_file_path(rel_file_path=rel_file_path,
                                                      style=style, anon=anon)
                with open(abs_path, read_mode) as f:
                    yield {"path": rel_file_path, "content": f.read()}
            else:
                raise ValueError(rel_file_path+" is not a valid relative file path or url.")

    @_option_validator()
    def put_files(self, files_on_local, style="rel_path", anon=False,
                  overwrite=False, return_paths="input", return_content=False,
                  read_mode="r"):
        """
        Copies the files defined in `files_on_local` to the sever.
        After 'uploading' the files it returns a list of paths or
        content_dicts depending on `return_content`

        Parameters
        ----------
        files_on_local: str, dict, list of str/dict, iterable of str/dict
            Path/-s to the local file/-s which should be copied to the server.

            str/list of str:
                all files will be copied to the chosen root.

            dict/list of dict:
                files_on_local["src"]:
                    gives the local file path and

                files_on_local["dest"]:
                    gives the relative path the file on the server.

        style: {'rel_path', 'url'}, default 'rel_path'
            'rel_path':
                path relative to server_home/anon_root is returned.

            'url':
                url to the file is returned.

        anon: bool
            True:
                Use anon_root as basepath

            False:
                Use server_home as basepath

        overwrite: bool, default False
            True:
                overwrites file without warning

            False:
                warns the user if a file exists and doesn't overwrite it

        return_paths: {'all', 'input', 'new'}, default 'input'
            'all':
                Return all files in the server_home/anon_root.

            'input':
                Return files in the server_home/anon_root,
                which were added by put_files.

            'new':
                Return only changed files in the server_home/anon_root,
                which were added by put_files.

        return_content: bool, default False
            False:
                Elements of the iterable to be returned will consist of only
                the paths (str).

            True:
                Elements of the iterable to be returned will consist of content_dicts.

        read_mode: {'r', 'rb'}, default 'r'
            This only applies if `return_content` is True.
            Mode in which files should be read (see ``open("filepath", read_mode)`` )


        Returns
        -------
        file_list: list
            List of filepaths/content dicts in server_home/anon_root

        Raises
        ------
        TypeError
            If `files_on_local` is not a ``str``, ``dict`` or ``iterable of str/dict``
        TypeError
            If `style` is not a ``str``
        TypeError
            If `anon` is not a ``bool``
        TypeError
            If `overwrite` is not a ``bool``
        TypeError
            If `return_paths` is not a ``str``
        TypeError
            If `return_content` is not a ``bool``
        TypeError
            If `read_mode` is not a ``str``

        ValueError
            If `files_on_local` is/contains an invalid filepath.
        TypeError
            If the value of `style` is not 'rel_path' or 'url'
        TypeError
            If the value of `return_paths` is not 'all', 'input' or 'new'
        TypeError
            If the value of `read_mode` is not 'r' or 'rb'

        KeyError
            If dict or list of dicts is used for `files_on_local` and the dict is
            missing the keys 'src' and 'dest'.

        Examples
        --------

        >>> ftpserver.put_files("test_folder/test_file", style="rel_path", anon=False)
        ["test_file"]

        >>> ftpserver.put_files("test_folder/test_file", style="url", anon=False)
        ["ftp://fakeusername:qweqwe@localhost:8888/test_file"]

        >>> ftpserver.put_files("test_folder/test_file", style="url", anon=True)
        ["ftp://localhost:8888/test_file"]

        >>> ftpserver.put_files({"src": "test_folder/test_file",
        ...                      "dest": "remote_folder/uploaded_file"},
        ...                     style="url", anon=True)
        ["ftp://localhost:8888/remote_folder/uploaded_file"]

        >>> ftpserver.put_files("test_folder/test_file", return_content=True)
        [{"path": "test_file", "content": "some text in test_file"}]

        >>> ftpserver.put_files("test_file.zip", return_content=True, read_mode="rb")
        [{"path": "test_file.zip", "content": b'PK\\x03\\x04\\x14\\x00\\x00...'}]

        >>> ftpserver.put_files("test_file", return_paths="new")
        UserWarning: test_file does already exist and won't be overwritten.
            Set `overwrite` to True to overwrite it anyway.
        []

        >>> ftpserver.put_files("test_file", return_paths="new", overwrite=True)
        ["test_file"]

        >>> ftpserver.put_files("test_file3", return_paths="all")
        ["test_file", "remote_folder/uploaded_file", "test_file.zip"]

        See Also
        --------
        get_file_contents
        get_file_paths
        """

        is_str_or_dict = isinstance(files_on_local, (str, dict))
        if is_str_or_dict or not isinstance(files_on_local, collections.Iterable):
            files_on_local = [files_on_local]

        base_path = self.get_local_base_path(anon=anon)
        file_list = []

        def append_file_path(file_path):
            """
            Helperfunction to reduce code overhead
            """
            rel_file_path = os.path.relpath(file_path, base_path)
            rel_file_path = self.format_file_path(rel_file_path, style=style, anon=anon)
            file_list.append(rel_file_path)

        for file_path_local in files_on_local:
            # implementation if a str path is used
            if isinstance(file_path_local, str):

                dirs, filename = os.path.split(file_path_local)
                file_path = os.path.abspath(os.path.join(base_path, filename))
                if not os.path.isfile(file_path_local):
                    raise ValueError(file_path_local+" is not a valid file path, "
                                                     "to an actual file.")
                if os.path.isfile(file_path) and not overwrite:
                    warnings.warn(UserWarning(file_path +
                                              " does already exist and won't be overwritten. "
                                              "Set `overwrite` to True to overwrite it anyway."
                                              ))
                else:
                    shutil.copyfile(file_path_local, file_path)
                    if return_paths == 'new':
                        append_file_path(file_path)
                if return_paths == 'input':
                    append_file_path(file_path)

            # implementation if a dict is used
            elif isinstance(file_path_local, dict):
                if "src" in file_path_local and "dest" in file_path_local:
                    dirs, filename = os.path.split(file_path_local["dest"])
                    dir_path = os.path.abspath(os.path.join(base_path, dirs))
                    # strip is needed in case dirs is " "
                    if dirs.strip() is not "" and not os.path.isdir(dir_path):
                        os.makedirs(dir_path)
                    file_path_local = file_path_local["src"]
                    file_path = os.path.abspath(os.path.join(base_path, dir_path, filename))

                    if not os.path.isfile(file_path_local):
                        raise ValueError(file_path_local+" is not a valid file path, "
                                                         "to an actual file.")
                    if os.path.isfile(file_path) and not overwrite:
                        warnings.warn(UserWarning(file_path +
                                                  " does already exist and won't be overwritten. "
                                                  "Set `overwrite` to True to overwrite it anyway."
                                                  ))
                    else:
                        # would have liked to use symlinks on posix to reduce copy overhead,
                        # but then you get permission errors since the file isn't in the
                        # users root dir (maybe some1 has an idea how to solve that :D )
                        shutil.copyfile(file_path_local, file_path)
                        if return_paths == 'new':
                            append_file_path(file_path)
                    if return_paths == 'input':
                        append_file_path(file_path)
                else:
                    raise KeyError("If dicts are used in `put_files`, the dicts "
                                   "need to have the Keys `src` and `dest`. "
                                   "The value of `src` needs to be a valid file path.")

            else:
                raise TypeError("`files_on_local` has to be of type a str or dict "
                                "or iterable of str/dict.")

        # this method uses return instead of a yield, because else files won't be copied
        # if the user wouldn't iterate over the values
        if not return_paths == 'all' and not return_content:
            return file_list
        elif not return_paths == 'all':
            return self.get_file_contents(file_list, style=style, anon=anon,
                                          read_mode=read_mode)
        elif not return_content:
            return self.get_file_paths(style=style, anon=anon)
        else:
            return self.get_file_contents(style=style, anon=anon,
                                          read_mode=read_mode)

    def stop(self):
        """
        Stops the server, closes all the open ports and deletes all temp files.
        This is especially useful if you want to test if your code behaves
        gracefully, when the ftpserver isn't reachable.

        Examples
        --------

        >>> ftpserver.stop()
        >>> your_code_connecting_to_the_ftp()
        RuntimeError: Server is offline/ not reachable.

        """
        self._server.stop()

    def __del__(self):
        self.stop()


class ThreadFTPServer(BaseMPFTPServer, threading.Thread):
    """
    Implementation of the server based on threading.Thread and BaseMPFTPServer
    (Windows and OSX).
    To learn about the functionality check out BaseMPFTPServer.
    """
    def __init__(self, username, password, ftp_home, ftp_port, **kwargs):
        # inheriting isn't done via super, since the strict order matters
        threading.Thread.__init__(self, **kwargs)
        BaseMPFTPServer.__init__(self, username, password,
                                 ftp_home, ftp_port)

    def run(self):
        self._server.serve_forever()


class ProcessFTPServer(BaseMPFTPServer, multiprocessing.Process):
    """
    Implementation of the server based on multiprocessing.Process and BaseMPFTPServer
    (Linux).
    To learn about the functionality check out BaseMPFTPServer.
    """
    def __init__(self, username, password, ftp_home, ftp_port, **kwargs):
        # inheriting isn't done via super, since the strict order matters
        multiprocessing.Process.__init__(self, **kwargs)
        BaseMPFTPServer.__init__(self, username, password,
                                 ftp_home, ftp_port)

    def run(self):
        # since the code run in a separate process can't be seen by
        # coverage this line doesn't need to be covered
        self._server.serve_forever()  # pragma: no cover

    def stop(self):
        self._server.stop()
        self.terminate()


@pytest.fixture(scope="module", autouse=True)
def ftpserver(request):
    """The returned ``ftpsever`` provides a threaded instance of
    ``pyftpdlib.servers.FTPServer`` running on localhost.  It has the following
    attributes:

    * ``ftp_port`` - the server port as integer
    * ``anon_root`` - the root of anonymous user
    * ``ftp_home`` - the root of authenticated user

    If you wish to control the credentials and home for the authenticated user,
    define in the test module the following 3 global variables:

    * ``ftp_username`` - login name (default: fakeusername).
    * ``ftp_password`` - login password (default: qweqweqwe).
    * ``ftp_home`` - the root for the authenticated user.

    Yields
    ------
    ftpserver: BaseMPFTPServer
        The type of `ftpserver` isn't actually `BaseMPFTPServer`,
        but a subclass with `threading.Thread` or `multiprocessing.Process`
        depending on the OS. But for autocomplete sake and since
        `BaseMPFTPServer` holds all functionality, let's pretend that it is
        `BaseMPFTPServer`.
    """
    ftp_user = os.getenv("FTP_USER", "fakeusername")
    ftp_password = os.getenv("FTP_PASS", "qweqwe")
    ftp_home = os.getenv("FTP_HOME", "")
    ftp_port = int(os.getenv("FTP_PORT", 0))
    if USE_PROCESS:
        server = ProcessFTPServer(ftp_user, ftp_password, ftp_home, ftp_port)
    else:
        server = ThreadFTPServer(ftp_user, ftp_password, ftp_home, ftp_port)
    # This is a must in order to clear used sockets
    server.daemon = True
    server.start()
    yield server
    server.stop()


if __name__ == "__main__":
    server = SimpleFTPServer("fakeusername", "qweqwe")
    print("FTPD running on port %d" % server.ftp_port)
    print("Anonymous root: %s" % server.anon_root)
    print("Authenticated root: %s" % server.ftp_home)
    server.serve_forever()
