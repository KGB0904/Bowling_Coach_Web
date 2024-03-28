import cv2
import os
import csv
import time
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 파일 경로 설정
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path = os.path.join(root_path, "data")
mp4_path = os.path.join(data_path, "mp4")

filename = "bowling1.mp4"

video_path = os.path.join(mp4_path, filename)
csv_path = os.path.join(data_path, "csv")
Med_path = os.path.join(csv_path, "Mediapipe")
pixel_path=os.path.join(Med_path,"pixel")

csv_file_path = os.path.join(pixel_path, "bowling1.csv")

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)
last_time = time.time()
cnt = 0  # 0.2초당 확인된 횟수
frame_number = 0

# 손목 좌표를 저장할 CSV 파일 생성
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'X', 'Y'])  # 헤더 추가

    start_time = time.time()
    print(f"파일이름 : {filename}")
    print("Mediapipe 테스트 시작")
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("테스트 종료")
                break

            # 이미지 처리
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # 이미지 원본 복원
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 오른쪽 손목 랜드마크 가져오기
            right_wrist_landmark = None
            if results.pose_landmarks:
                right_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

            # 손목 점
            if right_wrist_landmark and right_wrist_landmark.visibility > 0.5:
                image_height, image_width, _ = image.shape
                x_px, y_px = int(right_wrist_landmark.x * image_width), int(right_wrist_landmark.y * image_height)
                cv2.circle(image, (x_px, y_px), 5, (0, 255, 0), -1)

                # 0.2초 간격으로 CSV 파일에 기록
                current_time = time.time()
                if current_time - last_time >= 0.2:
                    writer.writerow([frame_number, x_px, y_px])
                    last_time = current_time
                    cnt += 1

            frame_number += 1

            # 이미지 좌우 반전 및 출력
            cv2.imshow('Right Wrist Landmark', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

# CSV 파일을 읽어 이동 범위 계산
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 헤더 건너뛰기

    # 손목 이전 좌표 초기화
    prev_x_px, prev_y_px = None, None
    pixel_movements = []

    for row in csv_reader:
        frame_num, x_px, y_px = map(float, row)

        if prev_x_px is not None and prev_y_px is not None:
            # 이전 프레임에서 현재 프레임으로의 픽셀 이동 계산
            pixel_movement = np.sqrt((x_px - prev_x_px)**2 + (y_px - prev_y_px)**2)
            pixel_movements.append(pixel_movement)

        # 현재 좌표를 이전 좌표로 업데이트
        prev_x_px, prev_y_px = x_px, y_px

# 이동 범위 계산
mean_pixel_movement = np.mean(pixel_movements)
print(f"평균 픽셀 단위 이동량: {mean_pixel_movement}")

end_time = time.time()
duration = end_time - start_time

# 이동량 출력
print(f"{round(duration, 3)}초 동안 0.2초당 {cnt}번의 손목이 포착되었습니다.")
