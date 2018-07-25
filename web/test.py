#!/usr/bin/python

import sys
import requests

response = requests.get('http://www.google.fr')
if not response:
	print("Request failed!")
	sys.exit()

print(response.content)
