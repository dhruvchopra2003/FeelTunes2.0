import music_recommender.recommender
import emotion_detector.EmotionDetectiontestRunner

emotion = emotion_detector.EmotionDetectiontestRunner.detect_emote("model/emoticon_model.json",
                                                                   "model/emoticon_model.h5",
                                                                   "emotion_detector/haarcascade/haarcascade_frontalface_default.xml")

music_recommender.recommender.recommend(emotion, "data/data_moods.csv")
