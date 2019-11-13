from flask import Flask, request, jsonify
import sys
import io
import os
#from google.cloud import vision
#from google.cloud.vision import types
#from dateparser.search import search_dates
#from datetime import datetime
import json
import base64
from Date_Extractor import DateExtractor
#from skimage.io import imread, imsave

app = Flask(__name__) 


@app.route('/extract_date', methods=['POST'])
def extract_date():
	if request.headers['Content-Type'] == 'application/json':

		try:
			data = request.json

			os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='Vision-19881f0ba5e0.json'

			de = DateExtractor()

			try:
				#Extracting Text From the Given Receipt Image
				ext_text = de.processTextExtraction(base64.b64decode(data["base_64_image_content"]))

			except Exception as e:
				return jsonify({'error':str(e)})

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
			return jsonify({'error':str(e)})

	else:
		return 'Specify the Correct Content-Type'

if __name__ == '__main__':
    app.run(debug=True)
