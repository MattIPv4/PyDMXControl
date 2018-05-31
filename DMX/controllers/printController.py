from .transmittingController import transmittingController


class printController(transmittingController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _send_data(self, data):
        print(data)
