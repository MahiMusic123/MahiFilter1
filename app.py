import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import numpy as np

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'outputs/'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def color_transfer(reference, target):
    # Convert images to Lab color space
    ref_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2Lab).astype(np.float32)
    tar_lab = cv2.cvtColor(target, cv2.COLOR_BGR2Lab).astype(np.float32)

    # Compute mean and std dev for each channel
    ref_mean, ref_std = cv2.meanStdDev(ref_lab)
    tar_mean, tar_std = cv2.meanStdDev(tar_lab)

    # Transfer color
    result_lab = (tar_lab - tar_mean) / tar_std * ref_std + ref_mean
    result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)

    # Convert back to BGR color space
    return cv2.cvtColor(result_lab, cv2.COLOR_Lab2BGR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file uploads
        ref_file = request.files['reference']
        tar_file = request.files['target']

        if not ref_file or not tar_file:
            return "Both images are required!", 400

        # Save uploaded files
        ref_path = os.path.join(app.config['UPLOAD_FOLDER'], 'reference.jpg')
        tar_path = os.path.join(app.config['UPLOAD_FOLDER'], 'target.jpg')
        ref_file.save(ref_path)
        tar_file.save(tar_path)

        # Read images
        reference = cv2.imread(ref_path)
        target = cv2.imread(tar_path)

        # Resize target to match reference size
        target_resized = cv2.resize(target, (reference.shape[1], reference.shape[0]))

        # Perform color transfer
        output = color_transfer(reference, target_resized)

        # Save output image
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.jpg')
        cv2.imwrite(output_path, output)

        # Redirect to display result
        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/outputs/<filename>')
def outputs(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
