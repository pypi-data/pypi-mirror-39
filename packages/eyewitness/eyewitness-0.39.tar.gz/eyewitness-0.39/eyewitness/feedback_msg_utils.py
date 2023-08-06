import json
import six
from abc import ABCMeta, abstractmethod
from collections import namedtuple

from eyewitness.config import (FEEDBACK_BBOX, FEEDBACK_FALSE_ALERT)
from eyewitness.image_id import ImageId
from eyewitness.audience_id import AudienceId


BboxObjectFeedback = namedtuple('BboxObjectFeedback',
                                ['x1', 'y1', 'x2', 'y2', 'label', 'meta'])
Type_Serialization_Mapping = {
    FEEDBACK_BBOX: BboxObjectFeedback,
    FEEDBACK_FALSE_ALERT: None,  # pure false alert won't have feedback_msg_objs
}


class FeedbackMsg(object):
    """
    represent the Feedback msg

    init with feedback_dict :
    - audience_id (require): audience information e.g. {platform_id}_{user_id}
    - feedback_method: feedback_method str
    - image_id: image_id obj or string e.g. 'channel1::1541860141::jpg'
    - feedback_meta: feedback_meta str
    - feedback_msg_objs: List of objects List[tuple]
    - receive_time: int

    """
    def __init__(self, feedback_dict):
        # get feedback method
        self.feedback_method = feedback_dict.get('feedback_method', FEEDBACK_FALSE_ALERT)
        self.feedback_type = Type_Serialization_Mapping[self.feedback_method]
        self.feedback_dict = feedback_dict

    @property
    def image_id(self):
        """
        Returns
        -------
        image_id: str
            image_id
        """
        return self.feedback_dict.get('image_id')

    @property
    def audience_id(self):
        """
        Returns
        -------
        audience_id: str
            audience_id
        """
        return self.feedback_dict['audience_id']

    @property
    def receive_time(self):
        """
        Returns
        -------
        receive_time: int
            receive_time
        """
        return self.feedback_dict['receive_time']

    @property
    def feedback_msg_objs(self):
        """
        Returns
        -------
        feedback_msg_objs: List[object]
            List of feedback msg objs
        """
        feedback_msg_objs = self.feedback_dict.get('feedback_msg_objs', [])
        return [self.feedback_type(*i) for i in feedback_msg_objs]

    @property
    def feedback_meta(self):
        """
        Returns
        -------
        feedback_meta: str
            feedback meta information
        """
        return self.feedback_dict.get('feedback_meta')

    @property
    def is_false_alert(self):
        """
        Returns
        -------
        is_false_alert: bool
            image published information is false alert or not
        """
        return self.feedback_dict.get('is_false_alert', True)

    @classmethod
    def from_json(cls, json_str):
        feedback_json_dict = json.loads(json_str)
        feedback_json_dict['audience_id'] = AudienceId.from_str(feedback_json_dict['audience_id'])
        if feedback_json_dict['image_id']:
            feedback_json_dict['image_id'] = ImageId.from_str(feedback_json_dict['image_id'])
        return cls(feedback_json_dict)

    def to_json_dict(self):
        """
        Returns
        -------
        image_dict: dict
            the dict repsentation of detection_result
        """
        json_dict = dict(self.feedback_json_dict)
        json_dict['audience_id'] = str(json_dict['audience_id'])
        if json_dict['image_id']:
            json_dict['image_id'] = str(json_dict['image_id'])
        return json_dict


@six.add_metaclass(ABCMeta)
class FeedbackMsgHandler():
    def handle(self, feedback_msg):
        assert self.feedback_method == feedback_msg.feedback_method
        return self._handle(feedback_msg)

    @abstractmethod
    def _handle(self, feedback_msg):
        """
        abstract method for handle feedback_msg

        Parameters:
        -----------
        feedback_msg: FeedbackMsg
        """
        pass

    @property
    def feedback_method(self):
        raise NotImplementedError
