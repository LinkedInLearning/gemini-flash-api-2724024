import os
import mimetypes
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

script_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(script_dir, 'images')

image_filenames = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
load_images = [{
    'mime_type': mimetypes.guess_type(image_filename)[0],
    'data': open(os.path.join(image_dir, image_filename), 'rb').read(),
    'relative_path': f'images/{image_filename}'
} for image_filename in image_filenames]

with open('alt_tags.html', 'w') as f:
    for load_image in load_images:
        relative_path = load_image.pop('relative_path')
        prompt = f"Output an IMG tag using {relative_path} as the src and alt attribute with a detailed description. Don't use markdown."
        response = model.generate_content([prompt, load_image])
        f.write(response.text + '\n')