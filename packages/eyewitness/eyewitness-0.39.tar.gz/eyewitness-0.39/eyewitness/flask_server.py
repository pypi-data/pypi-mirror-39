import io

import flask_admin
import logging
from flask import Flask
from flask import request
from flask_admin.contrib.peewee import ModelView
from peewee import SqliteDatabase

from eyewitness.image_id import ImageId
from eyewitness.models.db_proxy import DATABASE_PROXY
from eyewitness.models.detection_models import (ImageInfo, BboxDetectionResult)
from eyewitness.image_utils import ImageHandler


class ObjectDetectionFlaskWrapper(object):
    def __init__(self, obj_detector, image_register, detection_result_handlers,
                 sqlite_db_path='test.sqlite', with_admin=False):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        app = Flask(__name__)
        self.app = app
        self.obj_detector = obj_detector
        self.detection_result_handlers = detection_result_handlers
        self.database = SqliteDatabase(sqlite_db_path)
        self.image_register = image_register
        DATABASE_PROXY.initialize(self.database)
        ImageInfo.create_table()
        BboxDetectionResult.create_table()

        if with_admin:
            admin = flask_admin.Admin(app, name='Example: Peewee')
            admin.add_view(ModelView(ImageInfo))
            admin.add_view(ModelView(BboxDetectionResult))

        @app.route("/detect_post_bytes", methods=['POST'])
        def detect_image_bytes_objs():
            image_id = ImageId.from_str(request.headers['image_id'])
            self.image_register.register_image(image_id, {})
            raw_image_path = request.headers.get('raw_image_path', None)

            # read data from Bytes
            data = request.data
            image_data_raw = io.BytesIO(bytearray(data))
            image_raw = ImageHandler.read_image_bytes(image_data_raw)

            if raw_image_path:
                ImageHandler.save(image_raw, raw_image_path)

            # detect objs
            detection_result = self.obj_detector.detect(image_raw, image_id)
            for detection_result_handler in self.detection_result_handlers:
                detection_result_handler.handle(detection_result)
            return "successfully detected"

        @app.route("/detect_post_path", methods=['POST'])
        def detect_image_file_objs():
            image_id = ImageId.from_str(request.headers['image_id'])
            self.image_register.register_image(image_id, {})
            raw_image_path = request.headers['raw_image_path']
            image_raw = ImageHandler.read_image_file(raw_image_path)
            detection_result = self.obj_detector.detect(image_raw, image_id)
            for detection_result_handler in self.detection_result_handlers:
                detection_result_handler.handle(detection_result)
            return "successfully detected"
