from contextlib import contextmanager

from dalloriam import filesystem
from dalloriam.docker.container import Container

from typing import Dict, Iterator

import os
import random
import string
import sh
import time


class DockerClient:

    def __init__(self, username: str = None, password: str = None, server: str = None) -> None:
        """
        Initializes the client
        Args:
            username (str): Docker repository username.
            password (str): Docker repository password.
            server (str): Docker repository URL.
        """
        self._username = username
        self._password = password
        self._server = server

        if (self._username and self._password) or self._server:
            self._login()

    @staticmethod
    def _format_image_name(image_name: str, tag: str) -> str:
        return f'{image_name}:{tag}'

    def _login(self) -> None:
        args = []

        if self._username:
            args += ['-u', self._username]

        if self._password:
            args += ['-p', self._password]

        if self._server:
            args.append(self._server)

        sh.docker('login', *args)

    def build(self, content_dir: str, image_name: str, tag: str = 'latest') -> None:
        """
        Builds a docker image from a directory.
        Args:
            content_dir (str): Path that contains the image-related files.
            image_name (str): Desired name of the built image.
            tag (str):        Desired tag of the built image.
        """
        with filesystem.location(os.path.abspath(content_dir)):
            sh.docker('build', '-t', self._format_image_name(image_name, tag), '.')

    def push(self, image_name: str, tag: str = 'latest') -> None:
        """
        Pushes a docker image to the target repository
        Args:
            image_name (str): Name of the image to push.
            tag (str): Tag of the image.
        """
        sh.docker('push', self._format_image_name(image_name, tag))

    @contextmanager
    def container(
            self,
            image_name: str,
            tag: str = 'latest',
            ports: Dict[int, int] = None,
            volumes: Dict[str, str] = None) -> Iterator[Container]:
        """
        Start a container with the specified configuration in a context.
        Args:
            image_name (str): Name of the image to start.
            tag (str): Tag of the image to start.
            ports (Dict[int, int]): Port mappings.
            volumes (Dict[str, str]): Volume mappings.

        Returns:
            Running container.
        """
        c = Container(image_name=image_name, tag=tag)
        c.start(ports, volumes)
        time.sleep(2)
        try:
            yield c
        finally:
            c.stop()
