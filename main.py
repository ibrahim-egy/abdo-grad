from flask import Flask, render_template, url_for, request, redirect, flash
import tensorflow as tf
import numpy as np
import warnings
from PIL import Image, UnidentifiedImageError
import matplotlib.pyplot as plt
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import datetime
import os
import imghdr

warnings.filterwarnings('ignore')
IMAGE_SIZE = (8, 12)  # Output display size as you want

PATH_TO_SAVED_MODEL = "saved_model"
print('Loading model...', end='')
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
print('Done!')

category_index = label_map_util.create_category_index_from_labelmap("./label_map.pbtxt", use_display_name=True)


def load_image_into_numpy_array(path):
    return np.array(Image.open(path))


app = Flask(__name__)
app.secret_key = "serakfbeerkbeer"

infections = {
    'unhealthy sooty mold': {
        "treat": "Spray With detergent Mixture",
        "link": "http://extension.msstate.edu/publications/information-sheets/the-plant-doctor-sooty-mold#:~:text=Once%20sooty%20mold%20is%20established,spray%20it%20on%20the%20plants.",
        'no_treatment': "auto"
    },
    'unhealthy_foliar gall midge': {
        "treat": "Biochemical Spray",
        "link": "https://plantix.net/en/library/plant-diseases/600301/mango-midge",
        'no_treatment': "auto"
    },
    'unhealthy insufficient nutrients': {
        "treat": "Adding More Nutrients",
        "link": "https://vikaspedia.in/agriculture/crop-production/integrated-pest-managment/ipm-for-fruit-crops/ipm-strategies-for-mango/nutritional-deficiencies-of-mango",
        'no_treatment': "auto"
    },
    'Mango': {
        'treat': "#",
        "link": "#",
        'no_treatment': "none"
    },
    'healthy': {
        'treat': "#",
        "link": "#",
        'no_treatment': "none"
    }
}

# get year for copyright
today = datetime.date.today()
year = today.strftime("%Y")


@app.route('/')
def home():
    return render_template('index.html', year=year)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':

        image = request.files['img']

        type = imghdr.what(image)
        if type != 'jpeg':
            if type is None:
                flash("That's not an Image.")
            else:
                flash(f"Sorry Cant Work With .{type}.")
                flash("Make Sure The Image Is In .jpg format.")

            return redirect(url_for('home'))

        image_path = f'static/images/{image.filename}'
        image.save(image_path)
        image_np = load_image_into_numpy_array(image_path)
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = detect_fn(input_tensor)

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
            category_index,

            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.4)
        plt.figure(dpi=200)
        plt.axis("off")
        plt.imshow(image_np_with_detections)
        plt.savefig('static/outputs/result.png', bbox_inches='tight', pad_inches=0)
        os.remove(image_path)

        # show image
        # im = Image.open("static/outputs/result.png")
        # im.show()
        classes = [cls for cls in detections['detection_classes'][detections['detection_scores'] > .4]]
        classes = [category_index.get(cls)['name'] for cls in classes]
        data = {}

        for i in range(len(classes)):
            name = f"{i + 1}_{classes[i]}"
            score = detections['detection_scores'][i] * 100
            score = "{:.2f}".format(score)
            data[name] = {
                "score": score,
                "treat": infections[classes[i]]['treat'],
                "more_info": infections[classes[i]]['link'],
                'show': infections[classes[i]]['no_treatment']
            }

        return render_template('result.html', img="static/outputs/result.png", data=data, year=year)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
