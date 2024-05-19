#Occlusion Handlin 성능 평가 코드
#SECOND초당 1번꼴로 손목을 추적했을 때 예측을 통한 추적이 가능한 무브넷보다 얼마나 덜 추적할 수 있는지


import cv2
import os
import csv
import time
import mediapipe as mp
from Etc.check_gpu import check_gpu

SECOND=10 #몇초 단위로 할건지

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 비디오 파일 경로 설정
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path = os.path.join(root_path, "data")
input_path = os.path.join(data_path, "input")
mp4_path = os.path.join(input_path, "mp4")

#csv 파일 경로 설정
output_path = os.path.join(data_path, "output")
Coo_path=os.path.join(output_path,"Coordinate")
Med_path=os.path.join(Coo_path,"Mediapipe")
arm_path=os.path.join(Med_path,"arm")

#################################################################
#mp4파일경로
filename="bowling1.mp4"
#csv 파일경로
csv_file_path = os.path.join(arm_path, "bowling1.csv")
#################################################################

sum_gpu=0
cnt_gpu=0

video_path = os.path.join(mp4_path, filename)
# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)
last_time = time.time()
cnt = 0  # SECOND초당 확인된 횟수
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
            sum_gpu+=check_gpu()
            cnt_gpu+=1
            
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

            check_sh=False
            check_el=False
            check_wr=False
            # 어깨  점
            if right_shoulder_landmark and right_shoulder_landmark.visibility > 0.5:
                image_height, image_width, _ = image.shape
                x_sh, y_sh = int(right_shoulder_landmark.x * image_width), int(right_shoulder_landmark.y * image_height)
                cv2.circle(image, (x_sh, y_sh), 5, (255, 0, 0), -1)
                check_sh=True

                

            # 팔꿈치 점
            if right_elbow_landmark and right_elbow_landmark.visibility > 0.5:
                image_height, image_width, _ = image.shape
                x_elbow, y_elbow = int(right_elbow_landmark.x * image_width), int(right_elbow_landmark.y * image_height)
                cv2.circle(image, (x_elbow, y_elbow), 5, (255, 0, 0), -1)
                check_el=True
                
            # 손목 점
            if right_wrist_landmark and right_wrist_landmark.visibility > 0.5:
                image_height, image_width, _ = image.shape
                x_px, y_px = int(right_wrist_landmark.x * image_width), int(right_wrist_landmark.y * image_height)
                cv2.circle(image, (x_px, y_px), 5, (0, 255, 0), -1)
                check_wr=True

                # SECOND초 간격으로 CSV 파일에 기록
                current_time = time.time()
                if current_time - last_time >= SECOND:
                    writer.writerow([frame_number, x_px, y_px])
                    last_time = current_time
                    cnt += 1
            
            # 어깨부터 팔꿈치까지 선 그리기
            if check_sh and check_el: 
                cv2.line(image, (x_sh, y_sh), (x_elbow, y_elbow), (255, 255, 255), 2)

            # 팔꿈치부터 손목까지 선 그리기
            if check_el and check_wr:
                cv2.line(image, (x_elbow, y_elbow), (x_px, y_px), (255, 255, 255), 2)


            frame_number += 1

            # 이미지 좌우 반전 및 출력
            cv2.imshow('Right Wrist Landmark', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    end_time = time.time()
    duration = end_time - start_time
    msg=f"During {round(duration, 3)} seconds, {cnt} wrist movements were captured every {SECOND} seconds."
    writer.writerow([msg,None,None])


# CSV 파일의 마지막 줄에 메시지 추가
print([f"{round(duration, 3)}초 동안 {SECOND}초당 {cnt}번의 손목이 포착되었습니다."])

avg_gpu=sum_gpu/cnt_gpu

print(f"평균 GPU 사용량 : {round(avg_gpu,3)}%")
# 리소스 해제
cap.release()
cv2.destroyAllWindows()
