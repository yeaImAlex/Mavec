import pandas as pd
import os
import cv2
from datetime import datetime
from CameraM import OakDCamera
import time

global imgList, steeringList
countFolder = 0
count = 0
imgList = []
steeringList = []
CM = OakDCamera()

# GET CURRENT DIRECTORY PATH
myDirectory = os.path.join(os.getcwd(), 'DataCollected')

# CREATE A NEW FOLDER BASED ON THE PREVIOUS FOLDER COUNT
while os.path.exists(os.path.join(myDirectory, f'IMG{str(countFolder)}')):
    countFolder += 1
newPath = myDirectory + "/IMG" + str(countFolder)
os.makedirs(newPath)

# SAVE IMAGES IN THE FOLDER
def saveData(img, steering):
    global imgList, steeringList
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).replace('.', '')
    fileName = os.path.join(newPath, f'Image_{timestamp}.jpg')
    cv2.imwrite(fileName, img)
    imgList.append(fileName)
    steeringList.append(steering)

# SAVE LOG FILE WHEN THE SESSION ENDS
def saveLog():
    global imgList, steeringList
    rawData = {'Image': imgList, 'Steering': steeringList}
    df = pd.DataFrame(rawData)
    df.to_csv(os.path.join(myDirectory, f'log_{str(countFolder)}.csv'), index=False, header=False)
    print('Log Saved')
    print('Total Images: ', len(imgList))

if __name__ == '__main__':
    time.sleep(1)
    for x in range(10):
        img = CM.get_video() 
        if img is not None:
            saveData(img, 0)
            cv2.waitKey(1)
            cv2.imshow('Image', img)
        else:
            print('Image is not captured')
    saveLog()
