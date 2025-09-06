# Watercolor Image Generator

## Overview
This project is a simple web application that transforms uploaded images into hyper-realistic watercolor paintings using Google's Gemini API. The application features a dark-themed frontend with image preview functionality and a rotating loader during processing.

## Features
- Upload an image and preview it before processing.
- Generate hyper-realistic watercolor paintings with detailed artistic prompts.
- Dark-themed aesthetic frontend.
- Rotating loader during image processing.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **API**: Google Gemini API

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:Arjunheregeek/water_color.git
   ```
2. Navigate to the project directory:
   ```bash
   cd water_color
   ```
3. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Add your Google Gemini API key to the `.env` file:
   ```properties
   gemini_api=YOUR_API_KEY
   ```
6. Run the backend server:
   ```bash
   python backend/app.py
   ```
7. Open the `frontend/index.html` file in your browser.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Feel free to fork the repository and submit pull requests for improvements or new features.

## Contact
For any inquiries, please contact [Arjunheregeek](mailto:arjunheregeek@example.com).
