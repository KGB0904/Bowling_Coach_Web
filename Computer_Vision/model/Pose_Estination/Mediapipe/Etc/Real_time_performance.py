import cv2
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)  # 비디오 0번으로 설정
start_time = time.time()
cnt = 0  # 0.2초당 확인된 횟수
frame_number = 0
target_count = 50

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
        right_elbow_landmark = None
        right_shoulder_landmark = None

        if results.pose_landmarks:
            right_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            right_elbow_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_shoulder_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        check_sh = False
        check_el = False
        check_wr = False
        # 어깨  점
        if right_shoulder_landmark and right_shoulder_landmark.visibility > 0.5:
            image_height, image_width, _ = image.shape
            x_sh, y_sh = int(right_shoulder_landmark.x * image_width), int(right_shoulder_landmark.y * image_height)
            cv2.circle(image, (x_sh, y_sh), 5, (255, 0, 0), -1)
            check_sh = True

        # 팔꿈치 점
        if right_elbow_landmark and right_elbow_landmark.visibility > 0.5:
            image_height, image_width, _ = image.shape
            x_elbow, y_elbow = int(right_elbow_landmark.x * image_width), int(right_elbow_landmark.y * image_height)
            cv2.circle(image, (x_elbow, y_elbow), 5, (255, 0, 0), -1)
            check_el = True

        # 손목 점
        if right_wrist_landmark and right_wrist_landmark.visibility > 0.5:
            image_height, image_width, _ = image.shape
            x_px, y_px = int(right_wrist_landmark.x * image_width), int(right_wrist_landmark.y * image_height)
            cv2.circle(image, (x_px, y_px), 5, (0, 255, 0), -1)
            check_wr = True

            # 어깨부터 팔꿈치까지 선 그리기
            if check_sh and check_el:
                cv2.line(image, (x_sh, y_sh), (x_elbow, y_elbow), (255, 255, 255), 2)

            # 팔꿈치부터 손목까지 선 그리기
            if check_el and check_wr:
                cv2.line(image, (x_elbow, y_elbow), (x_px, y_px), (255, 255, 255), 2)

            # 확인된 횟수 증가
            cnt += 1

        frame_number += 1

        # 이미지 좌우 반전 및 출력
        cv2.imshow('Right Wrist Landmark', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

        # 50번의 cnt가 달성되면 종료
        if cnt >= target_count:
            end_time = time.time()
            duration = end_time - start_time
            print(f"{target_count}번의 손목 포착을 완료하는 데 걸린 시간: 약 {round(duration,3)} 초")
            break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
