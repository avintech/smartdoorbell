import cv2
import numpy as np
import pickle
import time  # Use time to track how long the face has been unrecognized
import pyrebase
import os
import json

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
	last_upload_time = 0  # Initialize last upload time

	while True:
		# Capture frame-by-frame
		ret, frame = camera.read()
		if not ret:
			break

		# Convert frame to grayscale
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# Detect faces in the frame
		faces = face_cascade_classifier.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)

		for (x, y, width, height) in faces:
			# Region of interest in grayscale for face recognition
			roi_gray = gray_frame[y:y+height, x:x+width]
			
			# Recognize face
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
						if time.time() - last_upload_time > 60:
							last_upload_time = time.time()  # Update last upload time
							#upload into unknown face
							current_time_s = time.time()
							current_struct_time = time.localtime(current_time_s)
							formatted_datetime = str(time.strftime("%d%m%Y",current_struct_time))
							formatted_minute = str(time.strftime("%H%M",current_struct_time))
							dirName = uuid+"/unknownfaces/"+formatted_datetime+"/"
							if not os.path.exists(dirName):
								os.makedirs(dirName)
							print(formatted_datetime)
							output_filename = uuid+"/unknownfaces/"+formatted_datetime+"/"+formatted_minute+".jpg"
							showPic = cv2.imwrite(output_filename,frame)
							print(showPic)
							storage.child(output_filename).put(output_filename,login[2])
							file_url = storage.child(output_filename).get_url(login[2])
							data = {"name": output_filename, "url": str(file_url)}
							print(data)
							db.child(uuid).child("unknownfaces").child(formatted_datetime).child(formatted_minute).set(data)
		
			#Display the rectangle and name
			cv2.rectangle(frame, (x, y), (x+width, y+height), color, 2)
			cv2.putText(frame, recognized_name + " {:.2f}".format(confidence), (x, y), font_style, 1, color, 2, cv2.LINE_AA)
		cv2.imshow('frame', frame)
	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	camera.release()
	cv2.destroyAllWindows()