from flask import Flask, render_template, request, jsonify, redirect, url_for
from Identifier import Identifier
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
identifier = Identifier()
UPLOAD_FOLDER = 'static'

app = Flask(__name__, static_folder="static")
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/img/<filename>")
def return_img(filename):
    return redirect(url_for('static', filename=filename), code=301)

@app.route('/upload', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return redirect(f"/output?filename={filename}")
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route("/output")
def output():
	return render_template("output.html")

@app.route("/predict")
def predict_url():
	filename = request.args.get('filename')
	verdict, probablity = identifier.predict_image(f"./static/{filename}")
	data = {"verdict": verdict, "probablity": probablity}
	print(data)
	return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)