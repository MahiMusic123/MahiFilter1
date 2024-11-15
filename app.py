from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np

app = Flask(__name__)

# Set upload folder and output folder paths
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('process_image', filename=file.filename))
    return redirect('/')

@app.route('/process/<filename>')
def process_image(filename):
    # Apply color transfer logic here
    target_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Example: Load images using OpenCV (replace with your color transfer logic)
    reference_image = cv2.imread('reference_image.jpg')  # reference image
    target_image = cv2.imread(target_path)
    
    # Example processing: (Apply color transfer to the target image)
    target_image = apply_color_transfer(reference_image, target_image)

    # Save the processed image
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, target_image)
    
    return render_template('result.html', image_file='output.jpg')

def apply_color_transfer(reference, target):
    # Example color transfer logic (use your own algorithm here)
    return target  # Return modified target image

if __name__ == '__main__':
    app.run(debug=True)
