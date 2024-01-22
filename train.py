import os
import numpy as np 
from PIL import Image 
import cv2
import pickle
import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_image_data(encrypted_file_name, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(encrypted_file_name, 'rb') as file:
        iv = file.read(16)  # Read the iv out - the first 16 bytes
        encrypted_data = file.read()
    decrypted_padded_data = cipher.decrypt(encrypted_data)
    original_data = unpad(decrypted_padded_data, AES.block_size)
    return original_data

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

iv = 0x0008739a3043314e614c4b764f234189
biv = iv.to_bytes(16,'big')
key = 0xf188c2f6176502368ab346a0b40f1098ed350c3c46595e998147ab1db9d865b7
bkey = key.to_bytes(32, 'big')

baseDir = os.path.dirname(os.path.abspath(__file__))
imageDir = os.path.join(baseDir, "images")

currentId = 1
labelIds = {}
yLabels = []
xTrain = []

for root, dirs, files in os.walk(imageDir):
	print(root, dirs, files)
	for file in files:
		print(file)
		if file.endswith("enc"):
			encrypted_path = os.path.join(root, file)
			decrypted_image_data = decrypt_image_data(encrypted_path, bkey, biv)
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
for root, dirs, files in os.walk(imageDir):
    print(root, dirs, files)
    for file in files:
        print(file)
        if file.endswith("enc"):
            encrypted_path = os.path.join(root, file)
            decrypted_image_data = decrypt_image_data(encrypted_path, bkey, biv)
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

recognizer.train(xTrain, np.array(yLabels))
recognizer.save("trainer.yml")
print(labelIds)
