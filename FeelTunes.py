import music_recommender.recommender
import face_detection.EmotionDetectiontestRunner

emotion = face_detection.EmotionDetectiontestRunner.detect_emote()

music_recommender.recommender.recommend(emotion)
