import os
import cv2
import mediapipe as mp
from mediapipe.python.solutions.pose import PoseLandmark

# 미디어파이프의 Pose 모델 라이브러리 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 비디오 파일 경로 설정
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
data_path = os.path.join(root_path, "data")
video_path = os.path.join(data_path, "bowling1.mp4")

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 비디오 라이터 객체 생성
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), 
                      (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Pose 모델 초기화
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=2)

# 캡처된 비디오를 처리
while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img_h, img_w, _ = img.shape
    img_result = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Pose 모델에 이미지 전달하여 랜드마크 추출
    results = pose.process(img)
    
    # 오른쪽 손목 랜드마크 인덱스
    RIGHT_WRIST_INDEX = mp_pose.PoseLandmark.RIGHT_WRIST.value

    if results.pose_landmarks:
        # 랜드마크 좌표 추출
        landmark = results.pose_landmarks.landmark  
        
        # 오른쪽 손목의 x, y 좌표 가져오기
        right_wrist_x = landmark[RIGHT_WRIST_INDEX].x * img_w
        right_wrist_y = landmark[RIGHT_WRIST_INDEX].y * img_h
        
        # 오른쪽 손목 랜드마크 시각화
        mp_drawing.draw_landmarks(img_result, results.pose_landmarks, 
                                   mp.solutions.holistic.POSE_CONNECTIONS, 
                                   landmark_list=[results.pose_landmarks.landmark[RIGHT_WRIST_INDEX]],
                                   connection_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        print("오른쪽 손목 x좌표 : ", right_wrist_x)
        print("오른쪽 손목 y좌표 : ", right_wrist_y)
        

    cv2.imshow('AI Golf Coach', img_result)
    out.write(img_result)

    if cv2.waitKey(1) == ord('q'):
        break

pose.close()
cap.release()
out.release()
cv2.destroyAllWindows()
