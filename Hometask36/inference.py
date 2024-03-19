import io
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from PIL import Image
from transformers import AutoImageProcessor, Mask2FormerForUniversalSegmentation
from collections import defaultdict

# Load fine-tuned Mask2Former model for panoptic segmentation
checkpoint = "facebook/mask2former-swin-base-coco-panoptic"
processor = AutoImageProcessor.from_pretrained(checkpoint)
model = Mask2FormerForUniversalSegmentation.from_pretrained(checkpoint)


def draw_image(image, segmentation, segments_info):
    """
    Builds a image for panoptic segmentation based on arguments
    `segmentation` and `segments_info` of postprocessed results.

    Returned image is `matplotlib.figure.Figure` instanse.
    """
    segmentation = segmentation.numpy()
    segments_counter = defaultdict(int)

    # Get the color map for segment colors
    viridis = plt.get_cmap("viridis", len(segments_info))

    # Construct image for segmentation
    segmentation_colors = np.zeros(segmentation.shape + (3,), dtype="int")
    patches = []
    for segment in segments_info:
        segment_id = segment["id"]
        segment_label_id = segment["label_id"]

        # Get a specified color for each segment
        color = viridis(segment_id)[:3]
        rgb_color = viridis(segment_id, bytes=True)[:3]

        # Construct a label for each segment
        label = f"{model.config.id2label[segment_label_id]}-{segments_counter[segment_label_id]}"
        segments_counter[segment_label_id] += 1

        # Set a segment color and add a segment label
        segmentation_colors[segmentation == segment["id"], :] = rgb_color
        patches.append(mpatches.Patch(color=color, label=label))

    # Build an image from the original image and the image with segments
    img = segmentation_colors * 0.8 + np.array(image) * 0.2
    img = img.astype("int")

    # Create an image figure
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_axis_off()
    ax.legend(handles=patches, bbox_to_anchor=(1, 1), loc="upper left")
    
    return fig


def panoptic_segmentation(input_image):
    """
    Performs the panoptic segmentation of `input_image`.

    Returns `PIL` image with segmentation.
    """

    # Get the Mask2Former model and perprocess the input image
    processor, model = get_model(CHECKPOINT)
    inputs = processor(images=input_image, return_tensors="pt")

    # Make an inference
    with torch.no_grad():
        outputs = model(**inputs)
    results = processor.post_process_panoptic_segmentation(outputs, target_sizes=[input_image.size[::-1]])[0]

    # Build an output image with panoptic segmentation
    fig = draw_image(input_image, **results)
    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches="tight")
    return Image.open(buf)
