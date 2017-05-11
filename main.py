
#
# class OptionMock:
#     def __init__(self, name, title, value, constraint):
#         self.name = name
#         self.title = title
#         self.value = value
#         self.constraint = constraint
#
# class DeviceMock:
#
#     def __init__(self, name):
#         self.options = {'a': OptionMock("a", "option a", 5, None),
#                         'b': OptionMock("b", "option b", 'b', ['a', 'b', 'c']),
#                         'c': OptionMock("c", "option c", 50, (0, 100)),
#                         'd': OptionMock("d", "option d", 200, [100, 200, 300])}
#
#         self.name = name
#
#     def __str__(self):
#         return self.name
#
#
# #import pyinsane2
# class Pyinsane2Mock:
#     def __init__(self):
#         self.PyinsaneException = Exception()
#
#     def init(self):
#         pass
#
#     def get_devices(self):
#         return [DeviceMock("dev a"),
#                 DeviceMock("dev b"),
#                 DeviceMock("dev c"),
#                 DeviceMock("dev d")]

#pyinsane2 = Pyinsane2Mock()

import pyinsane2

from os.path import expanduser
home = expanduser("~")

pyinsane2.init()


def selectDevice(devices):
    selected_device = 0

    for idx, dev in enumerate(devices):
        print(idx, ") ", str(dev))

    while True:
        selected_device = int(input("0-{} ".format(len(devices)-1)))
        if(0 <= selected_device < len(devices)):
            break
        else:
            print("input invalid")

    return devices[selected_device]


def selectOptions(opts):
    print("Please configure scanner")

    options = dict()

    for opt in opts:
        print(opt.name, opt.title)
        try:
            value = str(opt.value)
        except pyinsane2.PyinsaneException as exc:
            value = ""

        while True:
            _input = input("{} - ({}) ".format(str(opt.constraint), value))
            if _input == "":
                _input = value
                break
            elif isinstance(opt.constraint, list):
                if _input in opt.constraint:
                    break
                else:
                    print("input invalid")
                    continue

            elif isinstance(opt.constraint, tuple):
                _input = float(_input)
                if opt.constraint[1] >= _input >= opt.constraint[0]:
                    break
                else:
                    print("input invalid")
                    continue
            else:
                break

        options[opt.name] = [_input, value]
        print("---------")

    return options


def selectFilePath():
    _input = input("Please input save path ({}) ".format(home))
    if(input == ""):
        return home
    else:
        return _input


def selectNameRoot():
    _input = input("Please select name root ({}) ".format("scan"))
    if(_input == ""):
        return "scan"
    else:
        return _input


def applyOptions(device, options):
    pass

def scan(device):
    print("scanning with device", str(device))


def saveImage(image, fileName, path):
    print("Saving", image, "to: ", path, fileName)



def main():
    device = selectDevice(pyinsane2.get_devices())
    options = selectOptions(device.options.values())
    applyOptions(device=device, options=options)

    filePath = selectFilePath()
    nameRoot = selectNameRoot()

    print("scanning will begin after you press <enter>")
    scan_count = 0
    while True:
        _input = input("(<enter> or <q+enter>) ")

        if(_input == ""):
            fileNumber = str(scan_count)
            fileNumber = "".join(['0'*(5-len(fileNumber)), fileNumber])
            fileName = "".join([nameRoot, fileNumber, ".tif"])
            print("Scanning ", fileName)
            image = scan(device)
            print("Done. Saving", fileName)
            saveImage(image, fileNumber, filePath)
            scan_count = scan_count + 1

            continue

        if(_input == "q"):
            print("Exiting")
            break



if __name__ == "__main__":
    main()