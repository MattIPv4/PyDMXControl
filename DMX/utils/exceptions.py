class LTPCollisionException(Exception):

    def __init__(self, channel_id: int):
        super().__init__("Channel {} has two different values assigned at the same timestamp.".format(channel_id))


class MissingArgumentException(ValueError):

    def __init__(self, argument: str, kwarg: bool = False):
        super().__init__("Argument '{}' ({}) missing from call.".format(
            argument, "Positional" if not kwarg else "Keyword"))
