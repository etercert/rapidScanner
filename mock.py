from PIL import Image
from collections import namedtuple
PyinsaneException = Exception()


def readMock():
    raise EOFError
    return


class ScanSessionMock:
    def __init__(self):
        scanMock = namedtuple('scanMock', ['read'])
        self.scan = scanMock(readMock)
        self.images = [Image.open('test_image.jpeg')]


class OptionMock:
    def __init__(self, name, title, value, constraint):
        self.name = name
        self.title = title
        self.value = value
        self.constraint = constraint


class DeviceMock:

    def __init__(self, name):
        self.options = {'a': OptionMock("a", "option a", 5, None),
                        'b': OptionMock("b", "option b", 'b', ['a', 'b', 'c']),
                        'c': OptionMock("c", "option c", 50, (0, 100)),
                        'd': OptionMock("d", "option d", 200, [100, 200, 300])}

        self.name = name

    def __str__(self):
        return self.name

    def scan(*args, **kwargs):
        return ScanSessionMock()


def get_devices():
    return [DeviceMock("dev a"),
            DeviceMock("dev b"),
            DeviceMock("dev c"),
            DeviceMock("dev d")]


def maximize_scan_area(dev):
    pass


def init():
    pass


def exit():
    pass
