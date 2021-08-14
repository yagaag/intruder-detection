# intruder-detection-firebase.py
# Created by Yagaagowtham P

# Import library files
import threading
import cv2
import numpy as np
import tensorflow as tf
import pyrebase

# Initialize firebase app
def init_firebase(config, user_email, user_password):

    # Initialize firebase app
    firebase = pyrebase.initialize_app(config)
    # Get a reference to the auth service
    auth = firebase.auth()
    # Log the user in
    if auth.sign_in_with_email_and_password(user_email, user_password):
        print("Firebase User Authentication successful")
    else:
        print("Firebase User Authentication failed!")
    # Return the firebase database
    return firebase.database()

if __name__ == "__main__":

    # Common params
    alert_status = 'OFF'
    intruder_status = False
    file_id = 0

    # Parameters for the firebase app
    config = {
      "apiKey": "xxxx",
      "authDomain": "xxxx",
      "databaseURL": "https://xxxx.firebaseio.com",
      "storageBucket": "xxxx.appspot.com"
    }
    user_id = 0
    user_email = "xxxx"
    user_password = "xxxx"

    # Parameters for the camera
    frame_rate = 24
    frame_width = 1280
    frame_height = 720
    frame_size = (frame_width, frame_height)

    # Initialize connection to the firebase database
    db = init_firebase(config, user_email, user_password)

    # Load the Object Detection model
    model = tf.saved_model.load('efficientdet', tags=None, options=None)
    print("Model loaded successfully")

    # To alert firebase for intruders
    def alert_firebase(message):
        if message == 'intruder':
            results = db.child("Users").child(str(user_id)).update({"intruder": "True"})

    # To look for intruders in an image
    def detect(image, confidence):
        global intruder_status
        found = False
        # Resize image
        img = cv2.resize(image, (640, 640))
        image_np = np.expand_dims(img, axis=0)
        # Run object detection
        detector_output = model(image_np)
        classes = detector_output["detection_classes"][0].numpy()[:20]
        scores = detector_output["detection_scores"][0].numpy()[:20]
        for i in range(20):
            # If a person is detected with a minimum confidence, start recording and alert firebase
            if classes[i] == 1.0 and scores[i] > confidence:
                intruder_status = True
                found = True
                threading.Thread(target=alert_firebase, args=('intruder',)).start()
                print("Intruder!")
                break
        if found == False:
            intruder_status = False

    # To monitor for and record intruders
    def camera():

        global file_id
        frame_count = 0
        record_switch = False

        print("Starting camera...")
        cap = cv2.VideoCapture(0)
        result = cv2.VideoWriter('recordings/recording_' + str(file_id) + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, frame_size)

        while True:
            r, img = cap.read()
            if intruder_status == True and record_switch == False:
                # Start recording
                result = cv2.VideoWriter('recordings/recording_' + str(file_id) + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, frame_size)
                record_switch = True
                file_id += 1
                result.write(img)
            elif intruder_status == True and record_switch == True:
                # Recording
                result.write(img)
            elif intruder_status == False and record_switch == True:
                # Stop Recording
                record_switch = False
                result.release()
            frame_count += 1
            # Run detection every 1 second
            if frame_count % frame_rate == 0:
                frame_count = 0
                threading.Thread(target=detect, args=(img,0.6)).start()

            cv2.imshow("Live Preview", img)
            if alert_status == 'OFF':
                break

        cap.release()
        cv2.destroyAllWindows()

    # To await changes in alert status of the firebase app
    def stream_handler(message):
        global alert_status
        # If user sets 'alert' to 'ON', start intruder detection
        if message["data"]['alert'] == "ON":
            alert_status = 'ON'
            camera()
        # If user sets 'alert' to 'OFF', stop intruder detection
        if message["data"]['alert'] == "OFF":
            alert_status = 'OFF'

    # Subscribe to firebase stream
    my_stream = db.child("Users").child.(user_id).stream(stream_handler)
