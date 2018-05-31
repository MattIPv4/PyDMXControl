class LTPCollisionException(Exception):

    def __init__(self, channel_id):
        super().__init__("Channel {} has two different values assigned at the same timestamp.".format(channel_id))