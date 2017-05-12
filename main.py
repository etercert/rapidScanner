import os
import os.path
from os.path import isdir

if "TEST" in os.environ:
    import mock
    pyinsane2 = mock
else:
    import pyinsane2

home = os.getcwd()


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
            if(opt.constraint is not None):
                value = opt.constraint[0]
            else:
                value = ""

        while True:
            _input = input("{} - ({}) ".format(str(opt.constraint), value))
            if _input == "":
                _input = value
                break
            elif isinstance(opt.constraint, list):
                valueType = type(opt.constraint[0])
                _input = valueType(_input)
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
    while True:
        _input = input("Please input save path ({}) ".format(home))
        if not _input:
            _input = home

        if not isdir(_input):
            print(_input, "is not valid directory path")
        else:
            break

    return _input


def selectNameRoot():
    _input = input("Please select name root ({}) ".format("scan"))
    if not _input:
        return "scan"
    else:
        return _input


def applyOptions(device, options):
    for name, value in options.items():
        if name is not None:
            if len(value) == 2 and value[0] != value[1]:
                try:
                    pyinsane2.set_scanner_opt(device, name, value)
                except:
                    print("setting option failed!")


def scan(device):
    print("scanning with device", str(device))
    scan_session = device.scan(multiple=False)
    try:
        while True:
            scan_session.scan.read()
    except EOFError:
        pass

    image = scan_session.images[-1]
    return image


def saveImage(image, filename, path):
    print('saving: ', image, 'to', os.path.join(path, filename))
    try:
        with open(os.path.join(path, filename), mode='xb') as f:
            image.save(f, format="TIFF")
    except FileExistsError as err:
        print("file already exists")


def main():
    device = selectDevice(pyinsane2.get_devices())
    pyinsane2.maximize_scan_area(device)
    options = selectOptions(device.options.values())
    applyOptions(device=device, options=options)

    print("will scan with following options:")
    for opt in device.options.values():
        try:
            print(opt.name, opt.value)
        except pyinsane2.PyinsaneException as exc:
            pass

    filePath = selectFilePath()
    nameRoot = selectNameRoot()

    print("scanning will begin after you press <enter>")
    scan_count = 0
    while True:
        _input = input("(<enter> or <q+enter>) ")

        if not _input:
            fileNumber = str(scan_count)
            fileNumber = "".join(['0'*(5-len(fileNumber)), fileNumber])
            fileName = "".join([nameRoot, fileNumber, ".tif"])
            print("Scanning ", fileName)
            image = scan(device)
            print("Done. Saving", fileName)
            saveImage(image, fileName, filePath)
            scan_count = scan_count + 1
            continue

        if _input == "q":
            print("Exiting")
            break


if __name__ == "__main__":
    pyinsane2.init()
    try:
        main()
    finally:
        pyinsane2.exit()
