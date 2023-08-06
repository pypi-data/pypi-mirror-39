import datetime
import io
import operator
import re
from unittest import mock

import ui

import pytest

RED = "\x1b[31;1m"
GREEN = "\x1b[32;1m"
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
BEGIN_TITLE = "\x1b]0;"
END_TITLE = "\x07"


def assert_equal_strings(a, b):
    return a.split() == b.split()


@pytest.fixture
def smart_tty():
    res = io.StringIO()
    res.isatty = lambda: True
    return res


@pytest.fixture
def dumb_tty():
    res = io.StringIO()
    res.isatty = lambda: False
    return res


@pytest.fixture
def toggle_timestamp():
    tcli.CONFIG["timestamp"] = True
    yield
    tcli.CONFIG["timestamp"] = False


def test_info_stdout_is_a_tty(smart_tty):
    tcli.info(tcli.red, "this is red", tcli.reset,
            tcli.green, "this is green",
            fileobj=smart_tty)
    expected = (RED + "this is red " + RESET +
                GREEN + "this is green" + RESET + "\n")
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_update_title(smart_tty):
    tcli.info("Something", tcli.bold, "bold", fileobj=smart_tty, update_title=True)
    expected = (BEGIN_TITLE + "Something bold" + END_TITLE +
                "Something " + BOLD + "bold" + RESET + "\n")
    actual = smart_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_stdout_is_not_a_tty(dumb_tty):
    tcli.info(tcli.red, "this is red", tcli.reset,
            tcli.green, "this is green",
            fileobj=dumb_tty)
    expected = "this is red this is green\n"
    actual = dumb_tty.getvalue()
    assert_equal_strings(actual, expected)


def test_info_characters(smart_tty):
    tcli.info("Doing stuff", tcli.ellipsis, "sucess", tcli.check, fileobj=smart_tty)
    actual = smart_tty.getvalue()
    expected = "Doing stuff " + RESET + "…" + " sucess " + GREEN + "✓"
    assert_equal_strings(actual, expected)


def test_timestamp(dumb_tty, toggle_timestamp):
    tcli.info("message", fileobj=dumb_tty)
    actual = dumb_tty.getvalue()
    match = re.match(r"\[(.*)\]", actual)
    assert match
    assert datetime.datetime.strptime(match.groups()[0], "%Y-%m-%d %H:%M:%S")


def test_record_message(message_recorder):
    tcli.info_1("This is foo")
    assert message_recorder.find("foo")
    message_recorder.reset()
    tcli.info_1("This is bar")
    assert not message_recorder.find("foo")


def test_read_input():
    with mock.patch('builtins.input') as m:
        m.side_effect = ["foo"]
        actual = tcli.read_input()
        assert actual == "foo"


def test_read_password():
    with mock.patch('getpass.getpass') as m:
        m.side_effect = ["bar"]
        actual = tcli.read_password()
        assert actual == "bar"


def test_ask_string():
    with mock.patch('builtins.input') as m:
        m.side_effect = ["sugar!", ""]
        res = tcli.ask_string("coffee with what?")
        assert res == "sugar!"
        res = tcli.ask_string("coffee with what?", default="milk")
        assert res == "milk"


def test_ask_password():
    with mock.patch('getpass.getpass') as m:
        m.side_effect = ["chocolate!", ""]
        res = tcli.ask_password("guilty pleasure?")
        assert res == "chocolate!"


def test_empty_password():
    with mock.patch('getpass.getpass') as m:
        m.side_effect = [""]
        actual = tcli.ask_password("Please enter your password or just press enter to skip")
        assert actual == ""


def test_ask_yes_no():
    """ Test that you can answer with several types of common answers """
    with mock.patch('builtins.input') as m:
        m.side_effect = ["y", "yes", "Yes", "n", "no", "No"]
        expected_res = [True, True, True, False, False, False]
        for res in expected_res:
            actual = tcli.ask_yes_no("coffee?")
            assert actual == res


def test_ask_yes_no_default():
    """ Test that just pressing enter returns the default value """
    with mock.patch('builtins.input') as m:
        m.side_effect = ["", ""]
        assert tcli.ask_yes_no("coffee?", default=True) is True
        assert tcli.ask_yes_no("coffee?", default=False) is False


def test_ask_yes_no_wrong_input():
    """ Test that we keep asking when answer does not make sense """
    with mock.patch('builtins.input') as m:
        m.side_effect = ["coffee!", "n"]
        assert tcli.ask_yes_no("tea?") is False
        assert m.call_count == 2


def test_ask_choice():
    class Fruit:
        def __init__(self, name, price):
            self.name = name
            self.price = price

    def func_desc(fruit):
        return fruit.name

    fruits = [Fruit("apple", 42), Fruit("banana", 10), Fruit("orange", 12)]
    with mock.patch('builtins.input') as m:
        m.side_effect = ["nan", "5", "2"]
        actual = tcli.ask_choice("Select a fruit", fruits,
                               func_desc=operator.attrgetter("name"))
        assert actual.name == "banana"
        assert actual.price == 10
        assert m.call_count == 3


def test_ask_choice_empty_input():
    with mock.patch('builtins.input') as m:
        m.side_effect = [""]
        res = tcli.ask_choice("Select a animal", ["cat", "dog", "cow"])
        assert res is None


def test_ask_choice_ctrl_c():
    with pytest.raises(KeyboardInterrupt):
        with mock.patch('builtins.input') as m:
            m.side_effect = KeyboardInterrupt
            tcli.ask_choice("Select a animal", ["cat", "dog", "cow"])


def test_quiet(message_recorder):
    tcli.setup(quiet=True)
    tcli.info("info")
    tcli.error("error")
    assert message_recorder.find("error")
    assert not message_recorder.find("info")


def test_color_always(dumb_tty):
    tcli.setup(color="always")
    tcli.info(tcli.red, "this is red", fileobj=dumb_tty)
    assert RED in dumb_tty.getvalue()


def test_color_never(smart_tty):
    tcli.setup(color="never")
    tcli.info(tcli.red, "this is red", fileobj=smart_tty)
    assert RED not in smart_tty.getvalue()
