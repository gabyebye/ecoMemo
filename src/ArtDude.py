import io
from PIL import Image
import requests

class ArtGen():
    def __init__(self):
        self.API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        self.headers = {"Authorization": "Bearer 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"}

    def query_gen_art_ai(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def generate_image(self, gen_prompt, filename):

        image_bytes = self.query_gen_art_ai({"inputs": gen_prompt})

        if image_bytes:
            # You can access the image with PIL.Image for example
            image = Image.open(io.BytesIO(image_bytes))
            # image.show()
            image.save(f'./src/assets/cards/{filename}')
        else:
            print("Failed to generate image.")

# ai = ArtGen()

# ai.generate_image("Converts sunlight into electricity for homes and businesses.", "file.png")