from DMX.controllers.transmittingController import transmittingController


class printController(transmittingController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _send__data(self, data):
        print(data)
