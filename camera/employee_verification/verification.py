import math
import os
import sys
import dlib
import face_recognition
import numpy as np
import re
from gui.settings.Settings import *

SectionLoc = retreiveSectionLoc()
SectionSizes = retreiveSectionSizes()
cam = cameraSource()

def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = ''
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        barcode_info = barcode.data.decode('utf-8')

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(barcode_info) < 8:
            barcode_info = ''

    return barcode_info


class Verification:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.barcode = None
        self.face_authentication = None
        self.encode_faces()
        self.sp = dlib.shape_predictor('models\\face_model\\shape_predictor_68_face_landmarks.dat')
        self.facerec = dlib.face_recognition_model_v1('models\\face_model\\dlib_face_recognition_resnet_model_v1.dat')

    def encode_faces(self):
        for image in os.listdir('models\\face_model\\train'):
            face_image = face_recognition.load_image_file(f"models\\face_model\\train\\{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print("IDs Found in DB: {}".format(self.known_face_names))

    def run_verification(self):
        video_capture = cv2.VideoCapture(cam)
        print("Camera Starts")

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()
            self.barcode = read_barcodes(frame)
            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                # rgb_small_frame = small_frame[:, :, ::-1]
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    self.face_authentication = ''
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        self.face_authentication = self.known_face_names[best_match_index]
                        self.known_face_names.clear()
                        confidence = face_confidence(face_distances[best_match_index])

                    # self.face_names.append(f'{self.face_authentication}({confidence})')
                    self.face_authentication = re.sub('.jpg|.png|.jpeg', '', self.face_authentication)

            self.process_current_frame = not self.process_current_frame

            # Display the resulting image
            cv2.namedWindow('Face Recognition', cv2.WINDOW_KEEPRATIO)
            cv2.imshow('Face Recognition', frame)
            cv2.resizeWindow('Face Recognition', SectionSizes["cameraframe"][0], SectionSizes["cameraframe"][1])
            cv2.moveWindow('Face Recognition', SectionLoc["bodyframe1"][0], SectionLoc["bodyframe1"][1])

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif self.face_authentication is not None:
                print("Employee Id from Face Authentication: " + self.face_authentication)
                break
            elif self.barcode != '':
                print("Employee Id from barcode: " + self.barcode)
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

        if self.barcode:
            print("Camera Stopped")
            return self.barcode
        else:
            print("Camera Stopped")
            return self.face_authentication
