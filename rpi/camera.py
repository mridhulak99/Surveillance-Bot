#Takes a photo when the range of the ultrasoic sensor is less than 20cm ie when motion is detected
#The photo is then uploaded to aws S3

import RPi.GPIO as GPIO
import time
from datetime import date, datetime
from time import sleep
import picamera
import os
import tinys3
import yaml
import pytz
import boto3
import requests

GPIO.setmode(GPIO.BCM)

TRIG = 16
ECHO = 18
i=0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)


#camera setup()
def setup():
	with open("config.yml", 'r') as ymlfile:
		cfg = yaml.load(ymlfile)

	# photo props
	image_width = cfg['image_settings']['horizontal_res']
	image_height = cfg['image_settings']['vertical_res']
	file_extension = cfg['image_settings']['file_extension']
	file_name = cfg['image_settings']['file_name']
	photo_interval = cfg['image_settings']['photo_interval'] 
	image_folder = cfg['image_settings']['folder_name']


	camera = picamera.PiCamera()
	camera.resolution = (image_width, image_height)
	camera.awb_mode = cfg['image_settings']['awb_mode']

	if not os.path.exists(image_folder):
		os.makedirs(image_folder)
		
def takepic(datetime):

	filename=datetime
	filepath = image_folder + '/' + file_name + file_extension

	if cfg['debug'] == True:
		print '[debug] Taking photo and saving to path ' + filepath
	camera.capture(filepath)
		
	if cfg['debug'] == True:
		print '[debug] Uploading ' + filepath + ' to s3'

	# Upload to S3
	conn = tinys3.Connection(cfg['s3']['access_key_id'], cfg['s3']['secret_access_key'])
	f = open(filepath, 'rb')
	conn.upload(filepath, f, cfg['s3']['bucket_name'],
		headers={
			'x-amz-meta-cache-control': 'max-age=60'
			})

		
	if os.path.exists(filepath):
	os.remove(filepath)
	data={
		"dateandtime":dateandtime,
		"url": = "https://s3.amazonaws.com/makeathonpis/images/"+dateandtime+".jpg",
		}
	requests.post(url = http://54.160.238.67:5000/newpic, data = data)
try:
    setup()
    while True:
		tz = pytz.timezone('Asia/Kolkata')
		now = datetime.now()
		now = now.replace(tzinfo = tz)
		now = now.astimezone(tz)
		datetime = now.astimezone(tz)

		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0:
			pulse_start = time.time()

		while GPIO.input(ECHO)==1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150

		distance = round(distance+1.15, 2)

		if (distance<20):
			print "distance:",distance,"cm"
			takepic(datetime)
		sleep(5)
     

