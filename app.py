from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os

app = Flask(__name__)

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
    # Example processing: Apply color transfer (you would implement your logic here)
    target_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    reference_image = cv2.imread('reference_image.jpg')  # Replace with your reference image path
    target_image = cv2.imread(target_path)
    
    # Apply your color transfer logic here

    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, target_image)  # Replace with processed image
    
    return render_template('result.html', image_file='output.jpg')

if __name__ == '__main__':
    app.run(debug=True)
