import cv2
import numpy as np
from os import makedirs
from os.path import isdir

# save face
face_dirs = 'faces/'

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# extract face
def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3,5)

    # if no face
    if faces is():
        return None
    # Crop the face if have face
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    return cropped_face

# save only face
def take_pictures(name):
    # create folder if no folder of same name
    if not isdir(face_dirs+name):
        makedirs(face_dirs+name)

    # camera on
    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        # read a pic from camera
        ret, frame = cpa.read()

        if extract_face(frame) is not None:
            count+=1
            # transform size to 200*200
            face = cv2.resize(extract_face(frame), (200, 200))
            # change gray
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # save pic to 'faces/name/userxx.jpg'
            file_name_path = face_dirs + name + '/user'+str(count)+'.jpg'
            cv2.imwrite(file_name_path, face)

            cv2.putText(face, str(count), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2 )
            cv2.imshow('Face Cropper', face)
        else:
            print("Face not found")
            pass

        if cv2.waitKey(1) == 13 or count == 100:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Collecting Samples Complete')

if __name__ == "__main__":
    name = str(input())
    take_pictures(name)





