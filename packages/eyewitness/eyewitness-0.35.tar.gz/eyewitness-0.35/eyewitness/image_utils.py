import os
import six
import requests
from abc import ABCMeta

import numpy as np
import pkg_resources

from eyewitness.config import (POST_PATH, POST_BYTES)
from eyewitness.utils import make_path
from eyewitness.image_id import ImageId
from PIL import Image, ImageFont, ImageDraw

DEFAULT_FONT_PATH = pkg_resources.resource_filename('eyewitness', 'font/FiraMono-Medium.otf')


class ImageHandler(object):
    """
    common functions for image processing
    """
    @classmethod
    def save(cls, image, output_path):
        """
        Parameters:
        -----------
        image: PIL.Image
            image obj
        output_path: str
            path to be save
        """
        if isinstance(output_path, ImageId):
            output_path = str(output_path)
        folder = os.path.dirname(output_path)
        make_path(folder)
        image.save(output_path)

    @classmethod
    def read_image_file(cls, image_path):
        """
        Image.open read from file

        Parameters:
        -----------
        image_path: str
            source image path

        Return
        ------
        Image
            PIL.Image instance
        """
        return Image.open(image_path)

    @classmethod
    def read_image_bytes(cls, image_byte):
        """
        Image.open support BytesIO input

        Parameters:
        -----------
        image_path: BytesIO
            read image from ByesIO obj

        Return
        ------
        Image
            PIL.Image instance
        """
        return Image.open(image_byte)

    @classmethod
    def draw_bbox(cls, image, detections, colors=None, font_path=DEFAULT_FONT_PATH):
        """
        draw bbox on to image

        Parameters:
        -----------
        image: Image
            image to be draw
        detections: List[BoundedBoxObject]
            bbox to draw
        colors: Optional[dict]
            color to be used
        font_path: str
            font to be used
        """
        if colors is None:
            colors = {}

        font = ImageFont.truetype(
            font=font_path,
            size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 300

        for (left, top, right, bottom, predicted_class, score, _) in detections:
            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)

            # creating bbox on images
            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=colors.get(predicted_class, 'red'))
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=colors.get(predicted_class, 'red'))
            draw.text(text_origin, label, fill=(0, 0, 0), font=font)


@six.add_metaclass(ABCMeta)
class ImageProducer():
    def produce_method(self):
        raise NotImplementedError


class PostFilePathImageProducer(ImageProducer):
    def __init__(self, host, protocol='http'):
        self.protocol = protocol
        self.host = host

    def produce_method(self):
        return POST_PATH

    def produce_image(self, image_id, raw_image_path):
        headers = {'image_id': str(image_id),
                   'raw_image_path': raw_image_path}
        requests.post("%s://%s/detect_post_path" % (self.protocol, self.host), headers=headers)


class PostBytesImageProducer(ImageProducer):
    def __init__(self, host, protocol='http'):
        self.protocol = protocol
        self.host = host

    def produce_method(self):
        return POST_BYTES

    def produce_image(self, image_id, image_bytes, raw_image_path=None):
        headers = {'image_id': str(image_id)}

        if raw_image_path:
            headers['raw_image_path'] = raw_image_path

        requests.post(url="%s://%s/detect_post_bytes" % (self.protocol, self.host),
                      headers=headers,
                      data=image_bytes)


def swap_channel_rgb_bgr(image):
    """
    reverse the color channel image
    convert image (w, h, c) with channel rgb -> bgr
    convert image (w, h, c) with channel bgr -> rgb

    Parameters:
    -----------
    image: np.array
    """
    image = image[:, :, ::-1]
    return image
