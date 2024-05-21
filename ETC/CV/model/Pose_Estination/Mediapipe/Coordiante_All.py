import cv2
import os
import mediapipe as mp
import csv

from datetime import datetime, timedelta
from Etc.check_gpu import check_gpu

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path = os.path.join(root_path, "data")
input_path = os.path.join(data_path, "input")
mp4_path = os.path.join(input_path, "mp4")
video_path = os.path.join(mp4_path, "bowling1.mp4")


sum_gpu=0
cnt_gpu=0
#csv 파일 경로 설정
output_path = os.path.join(data_path, "output")
Coo_path=os.path.join(output_path,"Coordinate")
Med_path=os.path.join(Coo_path,"Mediapipe")
All_path=os.path.join(Med_path,"All")
csv_file_path = os.path.join(All_path, "bowling1.csv")

# 관심 있는 랜드마크 인덱스
landmark_mapping = {
    0: "nose",
    2: "left_eye",
    5: "right_eye",
    7: "left_ear",
    8: "right_ear",
    11: "left_shoulder",
    12: "right_shoulder",
    13: "left_elbow",
    14: "right_elbow",
    15: "left_wrist",
    16: "right_wrist",
    23: "left_hip",
    24: "right_hip",
    25: "left_knee",
    26: "right_knee",
    27: "left_ankle",
    28: "right_ankle",
}

# 미디어파이프를 초기화합니다.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# MP4 파일을 읽습니다.
cap = cv2.VideoCapture(video_path)


# CSV 파일을 열고 헤더를 작성합니다.
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'keypoint', 'x', 'y'])

# 재생 여부 플래그를 초기화합니다.
play = True
start_time = None

while cap.isOpened():
    # 재생 여부를 확인하고 비디오를 재생합니다.
    if play:
        ret, frame = cap.read()
        if not ret:
            break

    # 동영상이 시작된 후 1초 단위로 랜드마크 좌표를 기록합니다.
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # 밀리초를 초로 변환
    if start_time is None:
        start_time = current_time
        # 첫 프레임의 랜드마크 좌표도 기록합니다.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        sum_gpu+=check_gpu()
        cnt_gpu+=1
        if results.pose_landmarks:
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    if idx in landmark_mapping:
                        height, width, _ = frame.shape
                        cx, cy = int(landmark.x * width), int(landmark.y * height)
                        writer.writerow([start_time, landmark_mapping[idx], cx, cy])
        
    elif current_time - start_time >= 1:
        start_time = current_time
        # 미디어파이프로 포즈 추정을 수행합니다.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        # 결과를 확인하고 관심 있는 랜드마크를 CSV에 기록합니다.
        if results.pose_landmarks:
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    if idx in landmark_mapping:
                        height, width, _ = frame.shape
                        cx, cy = int(landmark.x * width), int(landmark.y * height)
                        timestamp = str(timedelta(seconds=start_time))
                        writer.writerow([timestamp, landmark_mapping[idx], cx, cy])

    # 키 이벤트를 처리합니다.
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('p'):
        play = not play

avg_gpu=sum_gpu/cnt_gpu
print(f"평균 GPU 사용량 : {round(avg_gpu,3)}%")

# 종료합니다.
cap.release()
cv2.destroyAllWindows()
