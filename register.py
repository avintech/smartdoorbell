import cv2
import numpy as np
import os
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256

# Encryption function
def encrypt_file(file_name, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(file_name, 'rb') as file:
        original_data = file.read()
    padded_data = pad(original_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    with open(file_name + ".enc", 'wb') as file:
        file.write(cipher.iv)
        file.write(encrypted_data)
    os.remove(file_name)  # Remove the original file

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Load the face cascade classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

name = input("What's his/her Name? ")
dirName = "./images/" + name
print(dirName)

if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory Created")
else:
    print("Name already exists")
    sys.exit()

count = 1

iv = 0x0008739a3043314e614c4b764f234189
biv = iv.to_bytes(16,'big')
key = 0xf188c2f6176502368ab346a0b40f1098ed350c3c46595e998147ab1db9d865b7
bkey = key.to_bytes(32, 'big')

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
        encrypt_file(fileName, bkey, biv)  # Encrypt the file
        cv2.imshow("face", roiGray)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count += 1

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)

    if key == 27 or count > 30:
        break

cap.release()
cv2.destroyAllWindows()
