from typing import Iterable, Dict

import random
import sh
import string


def _random_name(size: int = 12) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))


class Container:

    def __init__(self, image_name: str, tag: str) -> None:
        self.name = f'{image_name.split("/")[-1]}-{_random_name()}'
        self._image = f'{image_name}:{tag}'

    def start(self, ports: Dict[int, int] = None, volumes: Dict[str, str] = None) -> None:
        """
        Starts the container.
        Args:
            ports (Dict[int, int]): The port mappings.
            volumes (Dict[str, str]): The volume mappings.
        """
        ports_lst = []
        if ports is not None:
            for k, v in ports.items():
                ports_lst.append('-p')
                ports_lst.append(f'{k}:{v}')

        vol_lst = []
        if volumes is not None:
            for k, v in volumes.items():
                vol_lst.append('-v')
                vol_lst.append(f'{k}:{v}')

        sh.docker.run('--rm', '-d', *ports_lst, *vol_lst, '--name', self.name, self._image)

    def stop(self) -> None:
        """
        Stops the container.
        """
        sh.docker.stop(self.name)

    def exec(self, cmd: Iterable[str], background: bool = False) -> None:
        """
        Executes a command inside the container
        Args:
            cmd (Iterable[str]): The command arguments.
            background (bool): Whether to execute the command in the background or to await the results.
        """
        out = sh.docker.exec('-d' if background else '-i', self.name, *cmd)
        if not background:
            print(out)
