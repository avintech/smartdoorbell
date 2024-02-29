import os
import numpy as np 
from PIL import Image 
import cv2
import pickle
import io
from cryptography.fernet import Fernet
import pyrebase
import requests

firebaseConfig = {
				  'apiKey': "AIzaSyBeSc5ve2weKPGSk4Exgy5-VTBa4fGNPZQ",
				  'authDomain': "smartdoorbell-32ea3.firebaseapp.com",
				  'projectId': "smartdoorbell-32ea3",
				  'databaseURL':"",
				  'storageBucket': "smartdoorbell-32ea3.appspot.com",
				  'messagingSenderId': "884254413846",
				  'appId': "1:884254413846:web:bd13599244d7ec7abe5137",
				  'measurementId': "G-BBW763ZCEZ",
				  'serviceAccount': "smartdoorbell-32ea3-firebase-adminsdk-m8gtx-02c7f8f2b0.json"
				}
			  
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
storage = firebase.storage()    
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
		return [True,uuid]
	except Exception as error:
		print("Firebase error: ", error)
		return [False]
		
	  
def decrypt_image_data(key, filename):
	f = Fernet(key)
	with open(filename,"rb") as file:
		encrypted_data = file.read()
	decrypted_data = f.decrypt(encrypted_data)
	return decrypted_data

login = login()
if login[0] == True:
	uuid = login[1]
	
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
		all_files = storage.child(uuid+"/images/").list_files()
		#print("all folders: ",all_folders)
		for file in all_files:
			print("file: ",file.self_link)
			response = requests.get(file.media_link)
			if response.status_code == 200:
				directory = os.path.dirname(file.name)
				os.makedirs(directory, exist_ok=True)
				with open(file.name,'wb') as file:
					file.write(response.content)
					print("downloaded ",file.name," successfully!")			
	except Exception as error:
		print(error)
	
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