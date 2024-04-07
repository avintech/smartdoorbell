import cv2
import numpy as np
import pickle
import time  # Use time to track how long the face has been unrecognized
import pyrebase
import os
import json
from datetime import datetime
import requests
import json
import torch
import torchvision


# Load the YOLOv5 model outside of your main loop to avoid reloading it for each frame
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialize camera using 'camera' variable as you have been doing
camera = cv2.VideoCapture(0)  # Use the correct camera index

# Read the contents of the file
with open("data.txt", "r") as file:
	data = file.read()

# Replace single quotes with double quotes to make it valid JSON
data = data.replace("'", "\"")

# Load the JSON data
firebaseConfig = json.loads(data)
			  
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage = firebase.storage()
db = firebase.database()

last_upload_time = 0  # Initialize last upload time

#Function to check for camera obstruction
def is_camera_covered(frame, darkness_threshold=50, uniformity_threshold=0.5):
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	average_brightness = np.mean(gray_frame)
	unique, counts = np.unique(gray_frame, return_counts=True)
	uniformity = max(counts) / sum(counts) 
	if average_brightness < darkness_threshold or uniformity > uniformity_threshold: 
		return True
	else: 
		return False

def send_notification(last_upload_time, storage, db, uuid, login_2, frame, message):
	if (time.time() - last_upload_time) > 15:
		#upload image into database
		try:
			current_time_s = time.time()
			current_struct_time = time.localtime(current_time_s)
			formatted_datetime = str(time.strftime("%d%m%Y",current_struct_time))
			formatted_minute = str(time.strftime("%H%M",current_struct_time))
			dirName = uuid+"/unknownfaces/"+formatted_datetime+"/"
			if not os.path.exists(dirName):
				os.makedirs(dirName)
			output_filename = uuid+"/unknownfaces/"+formatted_datetime+"/"+formatted_minute+".jpg"
			cv2.imwrite(output_filename,frame)
			#upload to Firebase Storage
			storage.child(output_filename).put(output_filename,login_2)
			file_url = storage.child(output_filename).get_url(login_2)
			today_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
			date_unix_timestamp = int(today_date.timestamp())
			data = {"name": output_filename, "url": str(file_url)}
			#upload to Firebase Database
			db.child(uuid).child("unknownfaces").child(date_unix_timestamp).child(get_timestamp()).set(data)

		#create push notification to application
			with open('server.txt', 'r') as file:
				server_key = file.read()
			url = "https://fcm.googleapis.com/fcm/send"
			recipient = db.child(uuid).child("token").get().val()
			payload = json.dumps({
			"to": recipient,
			"notification": {
				"body": message,
				"title": "Enter to view."
			}
			})
			headers = {
				'Content-Type': 'application/json',
				'Authorization': 'key='+server_key
			}
			response = requests.request("POST", url, headers=headers, data=payload)
			print(response.text)
		except Exception as e:
			print("Error: ",e)
		finally:
			last_upload_time = time.time()  # Update last upload time
			return last_upload_time
	else:
		return last_upload_time
	
def login():
	print("Log in...")
	email=input("Enter email: ")
	password=input("Enter password: ")
	try:
		login = auth.sign_in_with_email_and_password(email, password)
		print("Successfully logged in!")
		print(auth.get_account_info(login['idToken']))
		uuid = auth.get_account_info(login['idToken'])['users'][0]['localId']
		print(uuid)
		return [True,uuid,login['idToken']]
	except Exception as error:
		print("Firebase error: ", error)
		return [False]

def get_timestamp():
    return int(datetime.now().timestamp())

login = login()
if login[0] == True:
	uuid = login[1]
	# Load the label dictionary
	with open('labels', 'rb') as label_file:
		label_dict = pickle.load(label_file)

	# Initialize face detection and recognition models
	face_cascade_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	face_recognizer.read("trainer.yml")
	font_style = cv2.FONT_HERSHEY_SIMPLEX

	# Initialize camera
	camera = cv2.VideoCapture(0)
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	recognition_threshold = 70  # Confidence threshold for recognizing a face
	unrecognized_time_threshold = 5  # Time in seconds after which to show "TOO LONG" message
	unrecognized_faces = {}  # Dictionary to keep track of unrecognized faces and their first appearance time
	
	while True:
		# Capture frame-by-frame
		ret, frame = camera.read()
		if not ret:
			break
		
		results = model(frame)

		detected_objects = results.pandas().xyxy[0]

		items_to_check = ["knife","fork","scissors","baseball bat"]
		detected_from_list = []

		# Check each item in your list against the detected objects
		for item in items_to_check:
			if any(detected_objects['name'].str.contains(item)):
				detected_from_list.append(item)
				
		if detected_from_list:
			print(f"Items detected from your list: {', '.join(detected_from_list)}")
			last_upload_time = send_notification(last_upload_time, storage, db, uuid, login[2], frame, "Dangeorous item detected")
			results.render()[0]
		else:
			print("No Dangerous Items")
	
		if is_camera_covered(frame):
			print("CAMERA IS OBSTRUCTED")
			last_upload_time = send_notification(last_upload_time, storage, db, uuid, login[2], frame, "Camera is obstructed")

		# Convert frame to grayscale
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# Detect faces in the frame
		faces = face_cascade_classifier.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)
		for (x, y, width, height) in faces:
			# Region of interest in grayscale for face recognition
			roi_gray = gray_frame[y:y+height, x:x+width]
			# Face Recognition
			face_id, confidence = face_recognizer.predict(roi_gray)
			if confidence <= recognition_threshold:
				# Loop through label dictionary to find the recognized face label
				recognized_name = ""
				for name, id_number in label_dict.items():
					if id_number == face_id:
						recognized_name = name
				color = (0, 255, 0)  # Green color for recognized faces
				print("hello, ", recognized_name)
				# If face is recognized, remove it from unrecognized_faces if it's there
				unrecognized_faces.pop(face_id, None)
			else:
				recognized_name = "Unknown"
				color = (0, 0, 255)  # Red color for unrecognized faces

				# Update the unrecognized_faces dictionary
				if face_id not in unrecognized_faces:
					unrecognized_faces[face_id] = time.time()
				else:
					# Check how long the face has been unrecognized
					duration_unrecognized = time.time() - unrecognized_faces[face_id]
					if duration_unrecognized > unrecognized_time_threshold:
						cv2.putText(frame, "TOO LONG", (x, y - 20), font_style, 1, (0, 0, 255), 2, cv2.LINE_AA)
						try:
							last_upload_time = send_notification(last_upload_time, storage, db, uuid, login[2], frame, "Unknown person at your door!")
						except Exception as ex:
							print(ex)
		
			#Display the rectangle and name
			cv2.rectangle(frame, (x, y), (x+width, y+height), color, 2)
			cv2.putText(frame, recognized_name + " {:.2f}".format(confidence), (x, y), font_style, 1, color, 2, cv2.LINE_AA)
		
		cv2.imshow('frame', frame)
		last_upload_time = last_upload_time
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	camera.release()
	cv2.destroyAllWindows()
