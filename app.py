import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

import parser

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['docx', 'pdf'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and \
	       filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
	return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	if file and allowed_file(file.filename):
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(file.filename)

		saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(saved_path)

		parsed_result = None

		if file.content_type == 'application/pdf':
			parsed_result = parser.parse_pdf(saved_path)
		elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
			parsed_result = parser.parse_docx(saved_path)

		print parsed_result

		# jsonify({'data': parsed_result})
		return redirect(url_for('uploaded_file', filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
	app.run(
		host="0.0.0.0",
		port=int("5000"),
		debug=True
	)