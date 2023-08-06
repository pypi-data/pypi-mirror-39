from linebot import LineBotApi
from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
    URIAction
)
from eyewitness.config import BBOX, LINE_FALSE_ALERT_MSG_TEMPLATE
from eyewitness.detection_utils import DetectionResultHandler


class LineAnnotationSender(DetectionResultHandler):
    def __init__(self, audience_ids, channel_access_token, image_url_handler,
                 detection_result_filter=None, detection_method=BBOX):
        """
        Parameters:
        -----------
        audience_ids: set
            line audience ids
        channel_access_token: str
            channel_access_token
        image_url_handler: Callable
            compose drawn image to image_url
        detection_result_filter: Callable
            a function check if the detection result to sent or not
        detection_method: str
            detection method
        """
        self.audience_ids = audience_ids
        self.line_bot_api = LineBotApi(channel_access_token)
        self.image_url_handler = image_url_handler
        self.detection_result_filter = detection_result_filter
        self._detection_method = detection_method

    @property
    def detection_method(self):
        return self._detection_method

    def _handle(self, detection_result):
        if self.detection_result_filter(detection_result):
            image_url = self.image_url_handler(detection_result.drawn_image_path)
            false_alert_feedback_text = LINE_FALSE_ALERT_MSG_TEMPLATE.format(
                image_id=str(detection_result.image_id), meta='')
            self.send_annotation_button_msg(image_url, false_alert_feedback_text)

    def send_annotation_button_msg(self, image_url, false_alert_feedback_text):
        """
        sent line botton msg to audience_ids

        Parameters:
        -----------
        image_url: str
            the url of image

        false_alert_feedback_text: str
            false_alert msg used to sent to feedback_handler
        """
        buttons_msg = TemplateSendMessage(
            alt_text='object detected',
            template=ButtonsTemplate(
                thumbnail_image_url=image_url,
                title='object detected',
                text='help to report result',
                actions=[
                    MessageAction(
                        label='Report Error (錯誤回報)',
                        text=false_alert_feedback_text
                    ),
                    URIAction(
                        label='full image (完整圖片)',
                        uri=image_url
                    )
                ]
            )
        )
        self.line_bot_api.multicast(list(self.audience_ids), buttons_msg)
