import cv2
from keras.models import model_from_json
import numpy as np


# loading weights

def detect_emote(json_path, model_path, cascade_path):
    max_index = 3
    emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprise"}

    json_file = open(json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    emotion_model = model_from_json(loaded_model_json)

    emotion_model.load_weights(model_path)
    print("loaded model from disc")

    # cap = cv2.VideoCapture("C:\\Users\\dhruv\\Desktop\\MusicRecommender\\face-detection\\sample-vid.mp4")
    cap = cv2.VideoCapture(0)
    # Opening the camera
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1280, 720))

        if not ret:
            break

        front_face_detector = cv2.CascadeClassifier(cascade_path)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #     detect faces on the camera
        num_faces = front_face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            # from the array of emotion predictions, taking key with maximum probability
            max_index = int(np.argmax(emotion_prediction))
            cv2.putText(frame, emotion_dict[max_index], (x + 5, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                        cv2.LINE_AA)

        cv2.imshow('Emotion Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return emotion_dict[max_index]


