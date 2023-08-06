import json
import six
from abc import ABCMeta, abstractmethod
from collections import namedtuple

from eyewitness.config import BBOX
from eyewitness.image_id import ImageId


BoundedBoxObject = namedtuple(
    'BoundedBoxObject', ['x1', 'y1', 'x2', 'y2', 'label', 'score', 'meta'])
Type_Serialization_Mapping = {BBOX: BoundedBoxObject}


class DetectionResult(object):
    """
    represent detection result of a image.

    init with feedback_dict :
    - detection_method: detection_method str
    - detected_objects: List[tuple]
    - drawn_image_path: path of drawn image str
    - image_id: image_id obj or string e.g. 'channel1::1541860141::jpg'

    """

    def __init__(self, image_dict):
        # get detection method
        self.detection_method = image_dict.get('detection_method', BBOX)
        self.detection_type = Type_Serialization_Mapping[self.detection_method]
        self.image_dict = image_dict

    @property
    def image_id(self):
        """
        Returns
        -------
        image_id: ImageId
            image_id
        """
        return self.image_dict['image_id']

    @property
    def drawn_image_path(self):
        """
        Returns
        -------
        drawn_image_path: str
            drawn_image_path
        """
        return self.image_dict.get('drawn_image_path', '')

    @property
    def detected_objects(self):
        """
        Returns
        -------
        detected_objects: List[object]
            List of detection results
        """
        detected_objects = self.image_dict.get('detected_objects', [])
        return [self.detection_type(*i) for i in detected_objects]

    @classmethod
    def from_json(cls, json_str):
        img_json_dict = json.loads(json_str)
        img_json_dict['image_id'] = ImageId.from_str(img_json_dict['image_id'])
        return cls(img_json_dict)

    def to_json_dict(self):
        """
        Returns
        -------
        image_dict: dict
            the dict repsentation of detection_result
        """
        json_dict = dict(self.image_dict)
        json_dict['image_id'] = str(json_dict['image_id'])
        return json_dict


@six.add_metaclass(ABCMeta)
class DetectionResultHandler():
    @abstractmethod
    def _handle(self, detection_result):
        """
        abstract method for handle DetectionResult

        Parameters:
        -----------
        detection_result: DetectionResult
        """
        pass

    def handle(self, detection_result):
        assert self.detection_method == detection_result.detection_method
        self._handle(detection_result)

    @property
    def detection_method(self):
        raise NotImplementedError
