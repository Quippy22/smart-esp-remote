import os
from posix import write

import ujson


class deviceDB:
    def __init__(self):
        self.path = "jsons"
        self.check_dir()

        self.devices = os.listdir(self.path)
        self.current_device = None

        self.buttons = None
        self.current_button = None

    def check_dir(self):
        # make dir for json files if it doesn't exist
        try:
            if (os.stat(self.path)[0] & 0x4000) != 0:
                # check if mode is directory
                return
        except OSError:
            os.mkdir("jsons")
            return

    def add_device(self, name):
        with open(f"{self.path}/{name}.json", "w") as f:
            f.write(ujson.dumps({}))

        # update the list of devices
        self.devices = os.listdir(self.path)

    def select_device(self):
        self.list_devices()

        # select device by index
        self.current_device = self.devices[
            int(input("Which device do you want to select? "))
        ]

    def list_devices(self):
        for i in range(len(self.devices)):
            print(i, " ", self.devices[i])

    def add_button(self, name, ir_code):
        # load the existing buttons
        with open(f"{self.path}/{self.current_device}", "r") as f:
            self.buttons = ujson.load(f)

        # add the new one
        self.buttons[name] = ir_code

        # save data in file
        with open(f"{self.path}/{self.current_device}", "w") as f:
            f.write(ujson.dumps(self.buttons))
