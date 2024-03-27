#0.2초당 손목 랜드마크 1회씩 뽑아내는 코드

import cv2, os, csv, time
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose



root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
data_path=os.path.join(root_path,"data")
mp4_path=os.path.join(data_path,"mp4")
video_path=os.path.join(mp4_path,"bowling1.mp4")
csv_path=os.path.join(data_path,"csv")
csv_file_path = os.path.join(csv_path, "recode.csv") #csv파일 경로

cap = cv2.VideoCapture(video_path)
last_time = time.time()
#one_last_time=time.time()
no_wrist_count = 0
start_time=time.time()
frame_number = 0
cnt=0   #0.2 초당 확인된 횟수

with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # 헤더를 추가합니다.
        writer.writerow(['Frame', 'X', 'Y'])

cnt=0   #1 초당 확인된 횟수
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    
    # CSV 파일을 쓰기 모드로 열고 csv writer를 생성합니다.
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # 헤더를 추가합니다.
        writer.writerow(['Frame', 'X', 'Y'])

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                #print("카메라를 찾을 수 없습니다.")
                print("테스트 종료")
                # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
                break

            # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # 손목 랜드마크를 그리기 전에 이미지를 원본으로 돌립니다.
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 오른쪽 손목의 랜드마크를 가져옵니다.
            right_wrist_landmark = None
            if results.pose_landmarks:
                right_wrist_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
                

            #############################################
            # 랜드마크가 감지되었는지 확인하고 좌표를 출력합니다.
            #감지
            #감지
            #감지
            #감지
            #############################################
            if right_wrist_landmark and right_wrist_landmark.visibility > 0.5:  # 랜드마크가 감지되었다면
                image_height, image_width, _ = image.shape
                x_px, y_px = int(right_wrist_landmark.x * image_width), int(right_wrist_landmark.y * image_height)
                
                # 오른쪽 손목 랜드마크를 그립니다.
                cv2.circle(image, (x_px, y_px), 5, (0, 255, 0), -1)
                current_time = time.time()
                if current_time - last_time >= 0.2:
                    print(x_px,y_px)
                    last_time = current_time
                    cnt+=1
                    writer.writerow([frame_number, x_px, y_px])

            frame_number += 1
            
            #else:
                # 손목 좌표가 감지되지 않은 경우 카운트 누적
                #손목 감지 카운트 시간 기준 : 1초
                #one_current_time=time.time()
                #if one_current_time - one_last_time >= 1:
                #    no_wrist_count += 1
                #    one_last_time=one_current_time
                    
            
            x_px=0
            y_px=0
            # 1초마다 카운트 출력
            #current_time = time.time()
            #if current_time - last_time >= 1:
                #맨 왼쪽위가 (0,0)
                #print(f'손목 좌표 감지 안됨 카운트 : {no_wrist_count}, ({int(x_px)}, {int(y_px)})')
                #print(x_px,y_px)
            #   last_time = current_time

            #이미지 보여주기
            cv2.imshow('Right Wrist Landmark', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

endtime=time.time()
term=endtime-start_time
print(f"{float(round(term,3))}초 동안 0.2초당 {cnt}만큼의 손목이 포착되었습니다.")
cap.release()
