from google.cloud import vision
from google.cloud.vision import types
from dateparser.search import search_dates
from datetime import datetime
import re

class DateExtractor:
	def __init__(self):
		self.client = vision.ImageAnnotatorClient()

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
			return ext_text
		else:
			return None

	def processDateExtraction(self,ext_text):
		mnths='jan|feb|mar|april|may|june|july|aug|sept|oct|nov|dec'

		#Types of Date Fromat to check in the Text
		date_patterns = [r'\d{1,2}[-|/|.|\s]\d{1,2}[-|/|.|\s](\d{4}|\d{2})',
						r'(\d{4}|\d{2})[-|/|.|\s]\d{1,2}[-|/|.|\s]\d{1,2}',
						r'\d{1,2}[-|/|.|\s|,]('+mnths+')[-|/|.|\s|,](\d{4}|\d{2})',
						r'('+mnths+')[-|/|.|\s|,]\d{1,2}[-|/|.|\s|,](\d{4}|\d{2})',]

		match=None
		date_str = ''

		for pat in date_patterns:
			match = re.search(pat, ext_text,re.IGNORECASE)
			if(match!=None):
				date_str = match.group()
				break

		if(match==None):
			return {'date': 'null'}
		else:
			#Returning Date in format YYYY-MM-DD
			return {'date': search_dates(date_str)[0][1].strftime("%Y-%m-%d")}


