import face_recognition
import cv2
import numpy as np
from io import BytesIO
from PIL import Image


from faces import Faces
from shoutout import ShoutOut

class Webcam():

    def __init__(self):
        self.running = False
        faces = Faces()
        self.known_face_encodings = faces.getKnownFaceEncodings()
        self.known_face_names = faces.getKnownFaceNames()

    def runDetection(self):
        #  includes some basic performance tweaks to make things run a lot faster:
        #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
        #   2. Only detect faces in every other frame of video.

        self.running = True

        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        shoutout = ShoutOut()

        # Create arrays of known face encodings and their names
        known_face_encodings = self.known_face_encodings
        known_face_names = self.known_face_names

        print('HERE WE GO')

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()


            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]['name']
                        shoutout.shoutRandom(known_face_names[first_match_index]['id'])

                    face_names.append(name)

            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        self.running = False
        video_capture.release()
        cv2.destroyAllWindows()

    def running(self):
        return self.running

    def detect_faces_in_image(self, file_stream):

        known_face_encodings = self.known_face_encodings
        known_face_names = self.known_face_names

        # Load the uploaded image file

        frame = np.array(file_stream)
        img = frame


        # Find all the faces and face encodings in the current frame of video
        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]['name']

            face_names.append(name)


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        pil_im = Image.fromarray(frame)
        return pil_im

