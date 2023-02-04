from flask import flash
import tensorflow as tf
import numpy as np
import warnings
from PIL import Image
import matplotlib.pyplot as plt
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import imghdr
from database import infections



def load_image_into_numpy_array(path):
    return np.array(Image.open(path))


def validate_image(image):
    image_type = imghdr.what(image)

    if image_type != 'jpeg':
        if image_type is None:
            flash("That's not an Image.")
        else:
            flash(f"Sorry Cant Work With .{image_type}.")
            flash("Make Sure The Image Is In .jpg format.")

        return True
    return False


class Detect:
    def __init__(self):
        warnings.filterwarnings('ignore')
        self.IMAGE_SIZE = (8, 12)  # Output display size as you want

        PATH_TO_SAVED_MODEL = "./saved_model"
        print('Loading model...', end='')
        self.detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
        print('Done!')

        self.category_index = label_map_util.create_category_index_from_labelmap("./label_map.pbtxt",
                                                                                 use_display_name=True)

    def detect(self, image_path):
        image_np = load_image_into_numpy_array(image_path)
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            self.category_index,

            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.4)
        plt.figure(dpi=200)
        plt.axis("off")
        plt.imshow(image_np_with_detections)

        plt.savefig('static/outputs/result.png', bbox_inches='tight', pad_inches=0)

        im = Image.open('static/outputs/result.png')
        im.thumbnail((500, 500))
        im.save('static/outputs/result_low.png')

        classes = [cls for cls in detections['detection_classes'][detections['detection_scores'] > .4]]
        classes = [self.category_index.get(cls)['name'] for cls in classes]
        data = {}

        for i in range(len(classes)):
            name = f"{i + 1}_{classes[i]}"
            score = detections['detection_scores'][i] * 100
            score = "{:.2f}".format(score)
            infection = infections.find_one({
                'name': classes[i]
            })
            print(infection)
            data[name] = {
                "score": score,
                "treat": infection['treat'],
                "more_info": infection['link'],
                'show': infection['no_treatment']
            }
        new_data = {}
        for item in data:
            class_name = item[2:]
            if class_name == "Mango":
                continue
            new_data[item] = data[item]
        return new_data
