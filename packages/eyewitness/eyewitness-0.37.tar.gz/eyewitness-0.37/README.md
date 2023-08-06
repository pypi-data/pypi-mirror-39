# EyeWitness
Lightweight Framework for ObjectDetection.
wrapper your own detector and add your handler.

system design:
https://drive.google.com/file/d/1x_sCFs91swHR1Z3ofS4e2KFz6TK_kcHb/view?usp=sharing


## env
implement with python3.6, i.e. detector should support python3.6, too.


## Installation
```bash
pip install eyewitness
```


## TODO
- add image producer(restricted with ImageId)
- add examples using more model(wrapper with docker, survey for lightweight/ more accurate model)
- add image_puller for image collection. (consumer design)
- support py2.7, py3.5, py3.7 and add CI for it.


## Things to be consider
[scale up]
- queuing system (how images pass(bytes(do by producer), file(queuing in fs))
- multiple detector


## unit-test
```
nose2
```

## a fake flask object detection example:
```
# start a server at http://localhost:5566/
# and a ADMIN made from flask-admin at http://localhost:5566/admin/
# you can implement your own ObjectDetector, DetectionResultHandler
python run_flask_server.py

# post pikachu image bytes to flask server
# which will stores raw pikachu.png and drawn pikachu_test.png at workspace


# post by channel
curl -X POST \
  http://localhost:5566/detect_post_bytes \
  -H 'content-type: application/json' \
  -H 'image_id: pikachu::1541860146::png'  \
  -H 'raw_image_path: ./pikachu_raw.png' \
  --data-binary "@eyewitness/test/pics/pikachu.png"


# post path of existing pikachu image file to flask server
# which will stores drawn pikachu.png at workspace
curl -X POST \
  http://localhost:5566/detect_post_path \
  -H 'content-type: application/json' \
  -H 'image_id: pikachu::1541860141::png' \
  -H 'raw_image_path: ./eyewitness/test/pics/pikachu.png'

# a python image producer (post_bytes) example
python post_bytes_image_producer.py

# a python image producer (post_path) example
python post_path_image_producer.py
```

## Line ResultHandler Example
```bash
# you can register your own Line Messaging API channel at https://developers.line.me
# make sure you have create line channel, and subscribe your own channel
export CHANNEL_ACCESS_TOKEN=<your-own-channel-tokenizer>
export YOUR_USER_ID=<your-line-user-id>
python line_detection_result_handler_example.py

# you should get a pikachu button annotation
```


## Real Detector example with docker
two examples: 
- RFB-SSD implemented by [lzx1413](https://github.com/lzx1413/PytorchSSD) with pytorch
- yolo-v3 implemented by [qqwweee](https://github.com/qqwweee/keras-yolo3) with keras

please take look at docker/RFB_detector/README.md, docker/YOLOv3_detector/README.md
which is eyewitness example that wrapper a detection model
