import gradio as gr

# This function is used to perform panoptic segmentation of an image
from inference import panoptic_segmentation


# Build a web app interface to use the Mask2Former model for panoptic segmentation
demo = gr.Interface(
    fn=panoptic_segmentation,
    inputs=gr.Image(type="pil", image_mode="RGB", label="Input image", show_label=True),
    outputs=gr.Image(type="pil", image_mode="RGB", label="Segmented image", show_label=True),
    title="Mask2Former Demo",
    description="This transformer-based model performs panoptic segmentation of the uploaded image"
)

if __name__ == "__main__":
    demo.launch(server_port=7000)
