# detection type
BBOX = 'bbox'

# Feedback type
FEEDBACK_BBOX = 'feedback_bbox'
FEEDBACK_FALSE_ALERT = 'feedback_false_alert'

# image producer type
POST_PATH = 'post_path'
POST_BYTES = 'post_bytes'
IN_MEMORY = 'in_memory'

# Line false_alert msg template
LINE_FALSE_ALERT_MSG_TEMPLATE = "false_alert_{image_id}_{meta}"
LINE_FALSE_ALERT_ANNOTATION_PATTERN = (
    r"false_alert_(?P<channel>.*)::(?P<timestamp>\d*)::(?P<file_format>.*)_(?P<meta>.*)")
