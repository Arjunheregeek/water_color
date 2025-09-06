import os
from flask import Flask, request, send_file, jsonify
from google import genai
from google.genai import types
import mimetypes
import base64
from io import BytesIO
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
API_KEY = os.getenv("gemini_api")
if not API_KEY:
    raise ValueError("API key not found in environment variables")

client = genai.Client(api_key=API_KEY)

# Enable CORS
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_data = image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="**Transform the PROVIDED INPUT IMAGE into a highly detailed and hyper-realistic watercolor painting.** The conversion must meticulously retain the original composition, subject matter, and intricate details of the given image, while completely adopting the aesthetic of a masterfully executed watercolor.\n\n**Artistic Style & Technique:**\nEmploy a sophisticated blend of traditional watercolor techniques. Focus on soft, feathered edges created by the 'wet-on-wet' method where appropriate, especially for backgrounds or atmospheric elements from the input image. Simultaneously, utilize precise 'wet-on-dry' brushwork to render sharp details, fine lines, and crisp edges on the main subjects of the input image. Achieve rich, vibrant colors through multiple transparent washes and glazes, building up depth and luminosity without becoming opaque or muddy. Show subtle, characteristic pigment granulation and natural color bleeding where colors meet on damp paper.\n\n**Texture & Medium:**\nThe final image must clearly exhibit the inherent textures of a high-quality, cold-press watercolor paper. This includes subtle visible fibers, slight tooth, and the way the pigment settles into the depressions of the paper. Simulate the natural pooling and drying patterns of watercolor, creating nuanced variations in color intensity across washes.\n\n**Lighting & Atmosphere:**\nRecreate the original input image's lighting, but enhance it with the ethereal glow and translucency characteristic of watercolor. Ensure light sources appear to refract gently through the transparent layers of paint. Shadows should be soft, layered, and colored, rather than dull and opaque. The overall atmosphere should be serene, artistic, and imbued with the unique, delicate beauty that only a watercolor medium can convey.\n\n**Realism & Fidelity:**\nThe goal is an artwork that, while distinctly a watercolor, feels incredibly real and tangible—as if it were meticulously hand-painted by a skilled artist onto physical paper. Maintain photorealistic fidelity to the original input image's subject and its emotional tone. Every element, from textures like skin, fabric, or foliage, to reflections and subtle surface variations, should be reinterpreted convincingly within the watercolor medium. The painting should look finished, professional, and ready for display in an art gallery.")
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        system_instruction=""
    )

    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-image-preview",
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
        ):
            part = chunk.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data') and part.inline_data:
                data_buffer = part.inline_data.data
                file_extension = mimetypes.guess_extension(part.inline_data.mime_type)
                file_name = f"output{file_extension}"
                file_name = os.path.join(os.path.dirname(__file__), file_name)

                print("DEBUG: Writing file", file_name)
                print("DEBUG: Data buffer size", len(data_buffer))

                with open(file_name, "wb") as f:
                    f.write(data_buffer)

                print("DEBUG: Sending file", file_name, "with MIME type", part.inline_data.mime_type)
                return send_file(file_name, mimetype=part.inline_data.mime_type)
            print("DEBUG: Part attributes:", dir(part))
            print("DEBUG: Part content:", part)

    return jsonify({'error': 'Failed to generate content'}), 500

if __name__ == '__main__':
    app.run(debug=True)
