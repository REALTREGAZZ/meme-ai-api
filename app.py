from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from diffusers import StableDiffusionPipeline
from PIL import Image
import torch

app = Flask(__name__)

# MODELOS GRATIS SIN TOKEN
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

image_pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

@app.route("/generate_meme", methods=["POST"])
def generate_meme():
    file = request.files["image"]
    image = Image.open(file).convert("RGB")

    # Generar caption
    inputs = caption_processor(image, return_tensors="pt")
    caption_ids = caption_model.generate(**inputs)
    caption = caption_processor.decode(caption_ids[0], skip_special_tokens=True)

    # Meme estilo brainrot
    meme_prompt = f"Brainrot meme, chaotic, zoomer humor, based on: {caption}"

    # Generar imagen meme
    result = image_pipe(meme_prompt).images[0]

    result.save("meme.png")
    return jsonify({"success": True, "caption": caption})
