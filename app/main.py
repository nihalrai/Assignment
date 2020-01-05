import os
import json
import csv
import time
import hashlib
import traceback
import urllib.request

from app import app
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, jsonify

# User Defined module
from process import Process

# Global variables
RUNNING_PROCESS = set()

# Process object for globally managing the threads of process
process_obj = Process()

def start_process(file):
    with open(file, 'w') as f:
        try:
            content = csv.reader(f)
            # time.sleep(40)
            # Run the thread of process.py
            process_obj.run(content, file)
        except:
            traceback.print_exc()
            pass

@app.route('/api/resume', methods=['GET'])
def resume_process():
    pid = request.args['pid']

    if pid is None or pid not in RUNNING_PROCESS:
	    resp = jsonify({'message' : 'Process Id not found'})
	    resp.status_code = 400
	    return json.dumps(resp, indent=4)

    elif pid in RUNNING_PROCESS:
        try:
            # Call resume function of Process class
            process_obj.resume()

            resp = jsonify({'message' : 'Process resumed successfully'})
            resp.status_code = 200
            return json.dumps(resp, indent=4)

        except:
            traceback.print_exc()
            resp = jsonify({'message' : 'Process cannot be resumed'})
            resp.status_code = 400
            return json.dumps(resp, indent=4)
    else:
        resp = jsonify({'message' : 'Invalid Request'})
        resp.status_code = 400
        return json.dumps(resp, indent=4)


@app.route('/api/stop', methods=['GET'])
def stop_process():
    pid = request.args['pid']

    if pid == '' or pid is None:
        resp = jsonify({'message' : 'Invalid Process Id found'})
        resp.status_code = 400
        return json.dumps(resp, indent=4)

    elif pid:
        try:
            # Call stop process of Process class
            process_obj.stop()

            resp = jsonify({'message' : 'Process stopped successfully'})
            resp.status_code = 200
            return json.dumps(resp, indent=4)

        except:
            traceback.print_exc()
            resp = jsonify({'message' : 'Process cannot be stopped'})
            resp.status_code = 400
            return json.dumps(resp, indent=4)

    else:
        resp = jsonify({'message' : 'Invalid Request'})
        resp.status_code = 400
        return json.dumps(resp, indent=4)


@app.route('/api/upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file found in request'})
		resp.status_code = 400
		return json.dumps(resp, indent=4)

	file = request.files['file']

	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return json.dumps(resp, indent=4)

	if file and 'png' in file.filename.split('.')[-1]:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		file_hash = hashlib.md5(file.filename.encode('utf-8')).hexdigest()

	    # Add the process in running set
		RUNNING_PROCESS.add(file_hash)

		resp = jsonify({
			'message' : 'File successfully uploaded',
			'pid': str(file_hash)
			})
		resp.status_code = 200

        	# start the process by calling start_process function
		start_process(file.filename)

		return json.dumps(resp, indent=4)

	else:
		resp = jsonify({'message' : 'Allowed file types is csv only.'})
		resp.status_code = 400
		return json.dumps(resp, indent=4)

if __name__ == "__main__":
    app.run()
