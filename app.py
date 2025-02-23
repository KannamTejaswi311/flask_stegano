from flask import Flask, render_template, request, send_file
from stegano import lsb
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hide', methods=['POST'])
def hide():
    if 'image' not in request.files or 'message' not in request.form:
        return "Missing image or message", 400
    
    image = request.files['image']
    message = request.form['message']
    
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    
    secret_image = lsb.hide(image_path, message)
    secret_image_path = os.path.join(UPLOAD_FOLDER, 'hidden.png')
    secret_image.save(secret_image_path)
    
    return send_file(secret_image_path, as_attachment=True)

@app.route('/reveal', methods=['POST'])
def reveal():
    if 'image' not in request.files:
        return "No image uploaded", 400
    
    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    
    message = lsb.reveal(image_path)
    return f"Hidden Message: {message}" if message else "No hidden message found"

if __name__ == '__main__':
    app.run(debug=True)
