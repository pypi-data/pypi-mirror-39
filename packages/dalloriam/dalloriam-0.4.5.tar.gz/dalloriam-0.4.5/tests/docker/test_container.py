from dalloriam import docker

from unittest import mock


def test_container_splits_name_properly():
    with mock.patch.object(docker.container, '_random_name', return_value='asdf'):
        c = docker.Container('some.domain.io/some_directory/some_image', 'latest')
        assert c.name == 'some_image-asdf'
