#미디어파이프와 무브넷 성능비교 코드 1
#0.2초당 몇번의 손목을 포착하는지
#output cs

import cv2
import os
import csv
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 파일 경로 설정
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path = os.path.join(root_path, "data")
mp4_path = os.path.join(data_path, "mp4")

filename="bowling1.mp4"

video_path = os.path.join(mp4_path, filename)
csv_path = os.path.join(data_path, "csv")
csv_file_path = os.path.join(csv_path, "Mediapipe_recode.csv")

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

            # 랜드마크가 감지되었으면 손목 좌표를 CSV에 기록
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

end_time = time.time()
duration = end_time - start_time

# CSV 파일의 마지막 줄에 메시지 추가
print([f"{round(duration, 3)}초 동안 0.2초당 {cnt}번의 손목이 포착되었습니다."])


# 리소스 해제
cap.release()
cv2.destroyAllWindows()
