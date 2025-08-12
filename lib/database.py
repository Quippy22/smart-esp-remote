import os

import ujson


class DeviceDB:
    def __init__(self):
        """
        Manages devices and their buttons stored as JSON files,
        using the 'jsons' directory to keep the project organized.

        Devices are stored as separate <device_name>.json files.
        Each file contains a dictionary of buttons where:
            - Key: Button name (str)
            - Value: IR code (str)

        Methods:
            - add(object, name, ir_code=None): Adds a device or button.
            - list(object): Lists all devices or buttons.
            - select(object): Selects a device or button via user input.
            - delete(object): Deletes a device or button via user input.

        'object' must be either 'device' or 'button', which determines the target.
        """

        self.path = "jsons"
        self.check_dir()

        self.devices = os.listdir(self.path)
        self.current_device = None

        self.buttons = {}
        self.current_button = {}

    def check_dir(self):
        """make sure there is a directory for the json files"""
        try:
            if (os.stat(self.path)[0] & 0x4000) != 0:
                # check if mode is directory
                return
        except OSError:
            os.mkdir("jsons")
            return

    def update(self):
        """Synchronize buttons and device list with JSON files"""
        # Update the devices list
        self.devices = os.listdir(self.path)

        # If a device is selected, update its file
        if self.current_device:
            with open(f"{self.path}/{self.current_device}", "w") as f:
                f.write(ujson.dumps(self.buttons))

    def manual_input(self, object, method):
        """temporary function for user input during testing"""
        if object == "device":
            self.list("device")
            return int(input(f"Which device do you want to {method}? "))
        else:
            self.list("button")

            # get name of selected button
            names = list(self.buttons.keys())

            # return the the button's key
            return names[int(input(f"Which button do you want to {method}? "))]

    def add(self, object, name, ir_code=None):
        if object == "device":
            with open(f"{self.path}/{name}.json", "w") as f:
                f.write(ujson.dumps({}))

        else:
            # add the new one
            self.buttons[name] = ir_code

        self.update()

    def delete(self, object):
        if object == "device":
            idx = self.manual_input(object, "delete")
            os.remove(f"{self.path}/{self.devices[idx]}")
        else:
            key = self.manual_input(object, "delete")
            del self.buttons[key]

        self.update()

    def list(self, object):
        if object == "device":
            for i in range(len(self.devices)):
                print(i, " ", self.devices[i])
        else:
            for i, name in enumerate(self.buttons):
                print(i, " ", name)

    def select(self, object):
        if object == "device":
            # select device by index
            self.current_device = self.devices[self.manual_input(object, "select")]

            # load the buttons of current device
            with open(f"{self.path}/{self.current_device}", "r") as f:
                self.buttons = ujson.load(f)
        else:
            # store selected values
            name = self.manual_input(object, "select")
            self.current_button = {name: self.buttons[name]}
