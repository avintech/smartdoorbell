import cv2
from cryptography.fernet import Fernet
import io
import json
import numpy as np
import os
import pickle
from PIL import Image 
import pyrebase
import requests
import sys

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

def decrypt_image_data(key, filename):
	f = Fernet(key)
	with open(filename,"rb") as file:
		encrypted_data = file.read()
	decrypted_data = f.decrypt(encrypted_data)
	return decrypted_data

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
	
# Encryption function
def encrypt_file(key, filename):
	f = Fernet(key)
	with open(filename, 'rb') as file:#rb means read in binary
		file_data = file.read()
		encrypted_data = f.encrypt(file_data)
	with open(filename,"wb") as file:
		file.write(encrypted_data)
	return filename
	
login = login()
if login[0] == True:
	uuid = login[1]
	# Initialize camera
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	# Load the face cascade classifier
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

	name = input("What's his/her Name? ")
	dirName = uuid + "/images/" + name
	
	print(dirName)

	if not os.path.exists(dirName):
		os.makedirs(dirName)
		print("Directory Created")
	else:
		print("Name already exists")
		sys.exit()

	count = 1


	while True:
		ret, frame = cap.read()
		if not ret:
			print("Failed to capture frame")
			break

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

		for (x, y, w, h) in faces:
			roiGray = gray[y:y + h, x:x + w]
			fileName = dirName + "/" + name + str(count) + ".jpg"
			cv2.imwrite(fileName, roiGray)
			encrypted_file = encrypt_file(b'yDrHaC4eMEzMchThHjlHGbpqkQyRsfr-xr0_ru94nUY=', fileName)  # Encrypt the file
			print(encrypted_file)
			#upload encrypted file
			storage.child(encrypted_file).put(encrypted_file, login[2])
			file_url = storage.child(encrypted_file).get_url(login[2])
			print(file_url)
			data = {"name": str(encrypted_file), "url": str(file_url)}
			print(data)
			db.child(uuid).child("images").child(name).push(data)
			print(encrypted_file)
			cv2.imshow("face", roiGray)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			count += 1

		cv2.imshow('frame', frame)
		key = cv2.waitKey(1)

		if key == 27 or count > 30:
			break

	cap.release()
	cv2.destroyAllWindows()

	#Train Model
	faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	
	baseDir = os.path.dirname(os.path.abspath(__file__))
	imageDir = os.path.join(baseDir,uuid, "images")
	#check if have local image
	if os.path.exists(imageDir):
		#remove if have
		print("Directory '",imageDir,"' exists. Removing it...")
		try:
			for root, dirs, files in os.walk(imageDir, topdown=False):
				for name in files:
					filepath = os.path.join(root,name)
					os.remove(filepath)
				for name in dirs:
					dirpath = os.path.join(root,name)
					os.rmdir(dirpath)
			os.rmdir(imageDir)
			
			parent_directory = os.path.dirname(imageDir)
			os.rmdir(parent_directory)
			print("Directory '",imageDir,"' removed successfully.")
		except OSError as e:
			print("Error: ",e)		
	
	#create uuid path if dont have
	os.makedirs(imageDir)
	print("Directory '",imageDir,"' created successfully.")
	try:
		all_recognised_face_name = db.child(uuid).child("images").get()
		for recognised_face_name in all_recognised_face_name.val():
			all_keys = db.child(uuid).child("images").child(recognised_face_name).get()
			for key in all_keys.each():
				data = key.val()
				response = requests.get(data['url'])
				if response.status_code == 200:
					directory = os.path.dirname(data['name'])
					os.makedirs(directory, exist_ok=True)
					with open(data['name'],'wb') as file:
						file.write(response.content)
						print("downloaded ",file.name," successfully!")			
	except Exception as error:
		print(error)
		exit()
	
	currentId = 1
	labelIds = {}
	yLabels = []
	xTrain = []

	for root, dirs, files in os.walk(imageDir):
		print(root, dirs, files)
		for file in files:
			if file.endswith("jpg"):
				print("root: ",root)
				print("file: ",file)
				encrypted_path = os.path.join(root, file)
				decrypted_image_data = decrypt_image_data(b'yDrHaC4eMEzMchThHjlHGbpqkQyRsfr-xr0_ru94nUY=', encrypted_path)
				# Convert the decrypted byte data to an image
				pilImage = Image.open(io.BytesIO(decrypted_image_data)).convert("L")
				imageArray = np.array(pilImage, "uint8")
				label = os.path.basename(root)
				print(label)

				if not label in labelIds:
					labelIds[label] = currentId
					print(labelIds)
					currentId += 1

				id_ = labelIds[label]
				imageArray = np.array(pilImage, "uint8")
				faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)

				for (x, y, w, h) in faces:
					roi = imageArray[y:y+h, x:x+w]
					xTrain.append(roi)
					yLabels.append(id_)

	with open("labels", "wb") as f:
		pickle.dump(labelIds, f)
		f.close()

	recognizer.train(xTrain, np.array(yLabels))
	recognizer.save("trainer.yml")
	print(labelIds)
