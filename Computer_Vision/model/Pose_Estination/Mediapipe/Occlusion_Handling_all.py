import cv2
import os
import csv
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 비디오 파일 경로 설정
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path = os.path.join(root_path, "data")
input_path = os.path.join(data_path, "input")
mp4_path = os.path.join(input_path, "mp4")

# csv 파일 경로 설정
output_path = os.path.join(data_path, "output")
Coo_path = os.path.join(output_path, "Coordinate")
Med_path = os.path.join(Coo_path, "Mediapipe")

#################################################################
# mp4파일경로
filename = "bowling1.mp4"
# csv 파일경로
csv_file_path = os.path.join(Med_path, "bowling1.csv")
#################################################################

video_path = os.path.join(mp4_path, filename)
# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)
last_time = time.time()
cnt = 0  # 0.2초당 확인된 횟수
frame_number = 0

# 손목 좌표를 저장할 CSV 파일 생성
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'Right Shoulder', 'Right Elbow', 'Right Wrist', 'Left Shoulder', 'Left Elbow', 'Left Wrist', 'Right Hip', 'Left Hip', 'Right Knee', 'Left Knee', 'Right Ankle', 'Left Ankle'])  # 헤더 추가

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

            # 포즈 랜드마크 가져오기
            right_shoulder_landmark = None
            right_elbow_landmark = None
            right_wrist_landmark = None
            left_shoulder_landmark = None
            left_elbow_landmark = None
            left_wrist_landmark = None
            right_hip_landmark = None
            left_hip_landmark = None
            right_knee_landmark = None
            left_knee_landmark = None
            right_ankle_landmark = None
            left_ankle_landmark = None

            if results.pose_landmarks:
                right_shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                right_elbow_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
                right_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                left_shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                left_elbow_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
                left_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
                right_hip_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                left_hip_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                right_knee_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
                left_knee_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
                right_ankle_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
                left_ankle_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]

            # 랜드마크 존재 여부 확인
            check_rs = False
            check_re = False
            check_rw = False
            check_ls = False
            check_le = False
            check_lw = False
            check_rh = False
            check_lh = False
            check_rk = False
            check_lk = False
            check_ra = False
            check_la = False

            # 오른쪽 어깨
            if right_shoulder_landmark and right_shoulder_landmark.visibility > 0.5:
                check_rs = True
                rs_x, rs_y = right_shoulder_landmark.x, right_shoulder_landmark.y

            # 오른쪽 팔꿈치
            if right_elbow_landmark and right_elbow_landmark.visibility > 0.5:
                check_re = True
                re_x, re_y = right_elbow_landmark.x, right_elbow_landmark.y

            # 오른쪽 손목
            if right_wrist_landmark and right_wrist_landmark.visibility > 0.5:
                check_rw = True
                rw_x, rw_y = right_wrist_landmark.x, right_wrist_landmark.y

            # 왼쪽 어깨
            if left_shoulder_landmark and left_shoulder_landmark.visibility > 0.5:
                check_ls = True
                ls_x, ls_y = left_shoulder_landmark.x, left_shoulder_landmark.y

            # 왼쪽 팔꿈치
            if left_elbow_landmark and left_elbow_landmark.visibility > 0.5:
                check_le = True
                le_x, le_y = left_elbow_landmark.x, left_elbow_landmark.y

            # 왼쪽 손목
            if left_wrist_landmark and left_wrist_landmark.visibility > 0.5:
                check_lw = True
                lw_x, lw_y = left_wrist_landmark.x, left_wrist_landmark.y

            # 오른쪽 엉덩이
            if right_hip_landmark and right_hip_landmark.visibility > 0.5:
                check_rh = True
                rh_x, rh_y = right_hip_landmark.x, right_hip_landmark.y

            # 왼쪽 엉덩이
            if left_hip_landmark and left_hip_landmark.visibility > 0.5:
                check_lh = True
                lh_x, lh_y = left_hip_landmark.x, left_hip_landmark.y

            # 오른쪽 무릎
            if right_knee_landmark and right_knee_landmark.visibility > 0.5:
                check_rk = True
                rk_x, rk_y = right_knee_landmark.x, right_knee_landmark.y

            # 왼쪽 무릎
            if left_knee_landmark and left_knee_landmark.visibility > 0.5:
                check_lk = True
                lk_x, lk_y = left_knee_landmark.x, left_knee_landmark.y

            # 오른쪽 발목
            if right_ankle_landmark and right_ankle_landmark.visibility > 0.5:
                check_ra = True
                ra_x, ra_y = right_ankle_landmark.x, right_ankle_landmark.y

            # 왼쪽 발목
            if left_ankle_landmark and left_ankle_landmark.visibility > 0.5:
                check_la = True
                la_x, la_y = left_ankle_landmark.x, left_ankle_landmark.y

            # 0.2초 간격으로 CSV 파일에 기록
            current_time = time.time()
            if current_time - last_time >= 0.2:
                writer.writerow([frame_number, check_rs*(rs_x, rs_y), check_re*(re_x, re_y), check_rw*(rw_x, rw_y),
                                 check_ls*(ls_x, ls_y), check_le*(le_x, le_y), check_lw*(lw_x, lw_y),
                                 check_rh*(rh_x, rh_y), check_lh*(lh_x, lh_y),
                                 check_rk*(rk_x, rk_y), check_lk*(lk_x, lk_y),
                                 check_ra*(ra_x, ra_y), check_la*(la_x, la_y)])
                last_time = current_time
                cnt += 1

            frame_number += 1

            # 이미지 좌우 반전 및 출력
            cv2.imshow('Pose Estimation', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    end_time = time.time()
    duration = end_time - start_time
    msg = f"During {round(duration, 3)} seconds, {cnt} wrist movements were captured every 0.2 seconds."
    writer.writerow([msg, None, None])


# CSV 파일의 마지막 줄에 메시지 추가
print([f"{round(duration, 3)}초 동안 0.2초당 {cnt}번의 손목이 포착되었습니다."])

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
