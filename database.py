import os

import ujson


class deviceDB:
    def __init__(self):
        """
        Manages devices and their buttons stored as JSON files, 
        using the 'jsons' directory to keep the project organized.

        Devices are stored as separate <device_name>.json files. 
        Each file contains a dictionary of buttons where:
            - Key: Button name (str)
            - Value: IR code (str)

        Methods:
            - add(obj_type, name, ir_code=None): Adds a device or button.
            - list(obj_type): Lists all devices or buttons.
            - select(obj_type): Selects a device or button via user input.

        obj_type must be either 'device' or 'button', which determines the target.
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

    def add(self, object, name, ir_code=None):
        """adds a device or button to the database"""

        if object == "device":
            with open(f"{self.path}/{name}.json", "w") as f:
                f.write(ujson.dumps({}))

            # update the list of devices
            self.devices = os.listdir(self.path)
        else:
            # add the new one
            self.buttons[name] = ir_code

            # save data in file
            with open(f"{self.path}/{self.current_device}", "w") as f:
                f.write(ujson.dumps(self.buttons))

    def list(self, object):
        if object == "device":
            for i in range(len(self.devices)):
                print(i, " ", self.devices[i])
        else:
            for i, name in enumerate(self.buttons):
                print(i, " ", name)

    def select(self, object):
        if object == "device":
            self.list("device")

            # select device by index
            self.current_device = self.devices[
                int(input("Which device do you want to select? "))
            ]

            # load the buttons of current device
            with open(f"{self.path}/{self.current_device}", "r") as f:
                self.buttons = ujson.load(f)
        else:
            self.list("button")

            # get name of selected button
            names = list(self.buttons.keys())
            name = names[int(input("Which button do you want to select? "))]

            # store selected values
            self.current_button = {name: self.buttons[name]}
