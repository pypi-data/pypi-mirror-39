import subprocess
import sys


def notification(title: str, message: str) -> None:
    """
    Sends a system notification.
    Args:
        title (str): The title of the notification
        message (str): The notification body.
    """
    if sys.platform == 'linux':
        subprocess.Popen(['notify-send', title, message])
    else:
        # TODO: Support macOS
        raise NotImplementedError
