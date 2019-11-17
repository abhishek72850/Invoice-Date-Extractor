from google.cloud import vision
from google.cloud.vision import types

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2

from dateparser.search import search_dates
from datetime import datetime
from skimage.io import imread, imsave
from dateparser.search import search_dates

import numpy as np

import sys
import re
import cv2 as cv
import base64

class DateExtractor:
	def __init__(self):
		self.client = vision.ImageAnnotatorClient()

	def processObjectDetection(self,base64_image):
		self.content = base64_image
		self.project_id = '125372421991'
		self.model_id = 'IOD6167596126800183296'

		prediction_client = automl_v1beta1.PredictionServiceClient()

		name = 'projects/{}/locations/us-central1/models/{}'.format(self.project_id, self.model_id)

		payload = {'image': {'image_bytes': self.content }}
		params = {}
		request = prediction_client.predict(name, payload, params).payload

		if(len(request)>0):
			if(request[0].display_name=='date'):
				c1,c2=request[0].image_object_detection.bounding_box.normalized_vertices

				nparr = np.fromstring(self.content, np.uint8)
				img = cv.imdecode(nparr, cv.IMREAD_COLOR)

				#img = cv.imread('renamed/'+f)
				#img = cv.cvtColor(img,cv.COLOR_BGR2RGB)

				width = img.shape[0]
				height = img.shape[1]

				x1 = int(c1.x*height)
				y1 = int(c1.y*width)
				x2 = int(c2.x*height)
				y2 = int(c2.y*width)

				retval, buffer = cv.imencode('.jpeg', img[y1:y2,x1:x2])
				jpg_as_text = base64.b64encode(buffer)

				return jpg_as_text

				#imsave('crop.jpeg'+f,img[y1:y2,x1:x2])
			else:
				return None
		else:
			return None

	def processTextExtraction(self,base64_image):
		self.content = base64_image
		try:
			image = vision.types.Image(content=self.content)
			response = self.client.text_detection(image=image)
		except Exception as e:
			return {'error':str(e)}
		
		texts = response.text_annotations

		if(len(texts)>0):
			ext_text = texts[0].description.replace('\n',' ')
			ext_text = ext_text.lower()
			return ext_text
		else:
			return None

	def processDateExtraction(self,ext_text):
		try:
			mnths = ['jan','january','feb','february','mar','march','apr','april','may','june',
					'jun','july','jul','aug','august','sept','september','oct','october','nov','november','dec','december']

			match = re.search(r'[a-z]+',ext_text,re.IGNORECASE)

			if(match!=None):
				if(match.group() not in mnths):
					for m in mnths:
						if(match.group() in m):
							ext_text = ext_text.replace(match.group(),m)
							break

			d_obj = search_dates(ext_text)

			if(d_obj!=None):
				date_str = d_obj[0][1].strftime("%Y-%m-%d")
				return {'date':date_str}
			else:
				return {'date':'null'}	
		except Exception as e:
			return {'date':'null'}