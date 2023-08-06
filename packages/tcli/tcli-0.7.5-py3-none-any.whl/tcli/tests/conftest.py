import ui
import re

import pytest


class MessageRecorder():
    def __init__(self):
        tcli.CONFIG["record"] = True
        tcli._MESSAGES = list()

    def stop(self):
        tcli.CONFIG["record"] = False
        tcli._MESSAGES = list()

    def reset(self):
        tcli._MESSAGES = list()

    def find(self, pattern):
        regexp = re.compile(pattern)
        for message in tcli._MESSAGES:
            if re.search(regexp, message):
                return message


@pytest.fixture()
def message_recorder(request):
    """ Start recording messages

    *Methods*

    * `stop()`: stop recording
    * `reset()`: clear the list of recorded messages.
    * `find(regex)` find a message in the list matching the given regular
       expression

    """
    recorder = MessageRecorder()
    yield recorder
    recorder.stop()
