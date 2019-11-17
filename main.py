from flask import Flask, request, jsonify
import sys
import io
import os
import json
import base64
from Date_Extractor import DateExtractor

app = Flask(__name__) 


@app.route('/extract_date', methods=['POST'])
def extract_date():
	if request.headers['Content-Type'] == 'application/json':

		try:
			data = request.json

			os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='Vision-19881f0ba5e0.json'

			de = DateExtractor()

			try:

				obj_detected = de.processObjectDetection(base64.b64decode(data["base_64_image_content"]))

				if(obj_detected != None):
					#Extracting Text From the Given Receipt Image
					ext_text = de.processTextExtraction(base64.b64decode(obj_detected))
				else:
					return jsonify({'date':'null'})

			except Exception as e:
				return jsonify({'error2':str(e)})

			if(ext_text!=None):
				if(type(ext_text)==dict):
					if('error' in ext_text.keys()):
						return jsonify(ext_date)
				else:
					#Extracting Date from the Extracted Text 
					ext_date = de.processDateExtraction(ext_text)
					return jsonify(ext_date)
			else:
				return jsonify({'date':'null'})

		except Exception as e:
			return jsonify({'error1':str(e)})

	else:
		return 'Specify the Correct Content-Type'

if __name__ == '__main__':
    app.run(debug=True)
