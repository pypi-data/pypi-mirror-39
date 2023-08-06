import six
from abc import ABCMeta, abstractmethod


class ImageId(object):
    """
    the target of ImageId is used to standardize the image_id format

    default init method from pattern {chanel}::{timestamp}::{fileformat}
    e.g: "channel::12345567::jpg"
    """

    def __init__(self, channel, timestamp, file_format='jpg'):
        """
        Parameters:
        -----------
        channel: str
            channel of image comes
        timestamp: int
            timestamp of image arrive time
        format: str
            type of image
        """
        self.timestamp = timestamp
        self.channel = channel
        self.file_format = file_format

    def __hash__(self):
        return hash(self.timestamp) ^ hash(self.channel) ^ hash(self.file_format)

    def __str__(self):
        # TODO make a more safer way
        return "{}::{}::{}".format(self.channel, str(self.timestamp), self.file_format)

    def __eq__(self, other):
        if isinstance(other, ImageId):
            return str(self) == str(other)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ImageId):
            return str(self) < str(other)
        return NotImplemented

    @classmethod
    def from_str(cls, image_id_str):
        # TODO make a more safer way
        channel, timestamp, file_format = image_id_str.split('::')
        return cls(channel=channel, timestamp=int(timestamp), file_format=file_format)


@six.add_metaclass(ABCMeta)
class ImageRegister():
    def register_image(self, image_id, meta_dict):
        raw_image_path = meta_dict.get('raw_image_path', None)
        self.insert_image_info(image_id, raw_image_path=raw_image_path)

    @abstractmethod
    def insert_image_info(image_id, raw_image_path):
        pass
