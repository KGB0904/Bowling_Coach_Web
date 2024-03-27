#수정예정 검색해서 코드 가져다 쓰기

import os
import cv2
import mediapipe as mp

#미디어파이프의 Pose 모델 라이브러리 

#랜드마크(관절포인트) 이미지에 그리기
mp_drawing = mp.solutions.drawing_utils

#랜드마크 표시하는 방법 즉, 그려지는 스타일 결정
mp_drawing_styles = mp.solutions.drawing_styles

#미디어파이프 포즈 제공, 포즈 추정 : 사용자가 어떤 포즈를 취하는지.
mp_pose = mp.solutions.pose

#data\bowling1.mp4 경로
root_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
data_path=os.path.join(root_path,"data")
video_path=os.path.join(data_path,"bowling1.mp4")




#비디오 캡처 객체 : 동영상 데이터를 어디서 가져올껀지
cap = cv2.VideoCapture(video_path)

#비디오 라이터 객체 생성
#MPEG-4 코덱 사용
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#출력파일명, 코덱, FPS, 프레임 크기 설정
#그니까 이건 output 영상 만드는 빙밥이다.
#cap.get(cv2.CAP_PROP_FPS) : 프레임 속도 가져오기, cv2.CAP_PROP_FPS : 비디오의 FPS
#cv2.CAP_PROP_FRAME_WIDTH : 비디오 프레임의 너비

out = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

#Mediapip pose모델 초기화
#탐지(detection) : 처음 발견하는데
#추적(tracking)  : 계속 따라가는데
pose = mp_pose.Pose(    
    min_detection_confidence=0.5,   #탐지 신뢰도 (신뢰도가 높은게 좋은게 아닌 이유 : 성능, 이 부분의 높은 의존도로 인한 따른 경우의 수 무시하는 상황 발생 우려)
    min_tracking_confidence=0.5,    #추적 신뢰도
    model_complexity=2)             #모델의 복잡도


#플래그 : 상태를 나타내는 bool 형태 변수
is_first = True # 어드레스 시 첫 프레임을 받아오기 위한 플래그

# 어드레스 시 첫 프레임의 좌표를 저장할 변수
#머리 중심의 x,y 그리고 반지름
first_center_x, first_center_y, first_radius = None, None, None

#캡처 : 비디오를 받아온 객체
while cap.isOpened():       #비디오 캡처 객체가 열려있는 동안 실행
    ret, img = cap.read()   #프레임 읽어오고 프레임을 이미지와 부울값으로 반환, ret : 프레임 읽었으면 true, img : 읽어온 프레임 이미지 자체 opencv의 mat객체 형태
    if not ret:             #프레임을 못읽는다면 혹은 다 읽었다면
        break               #종료

    img_h, img_w, _ = img.shape #이미지(프레임)의 높이, 너비, 채널 반환

    img_result = img.copy()     #원본 이미지 복사

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #이미지를 RGB형식으로 변환
    
    #pose : 이미 학습된 모델 객체
    #process() : 이미지를 pose모델에 전달하고 포즈 탐지한 처리결과 반환
        #랜드마크(관절 위치) 찾아내고 랜드마크 기반으로 사람의 자세 추정
    results = pose.process(img) 

#이미지안에 시각화, 즉 랜드마크 선으로 잇는 함수
    mp_drawing.draw_landmarks(
        img_result,                 #시각화할 이미지
        results.pose_landmarks,     #랜드마크 정보
        mp_pose.POSE_CONNECTIONS,   #랜드마크 연결선을 의미하는 상수
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()) #랜드마크 그릴 때 스타일 지정 - 기본 스타일

    if results.pose_landmarks:
        # https://google.github.io/mediapipe/solutions/pose.html#pose-landmark-model-blazepose-ghum-3d
        
        #랜드마크들의 리스트
        landmark = results.pose_landmarks.landmark  #랜드마크 좌표 추출

        #수정예정 만약 볼링을 하게된다면 이 부분 사용해서 관절 포인트 사용 가능
        left_ear_x = landmark[mp_pose.PoseLandmark.LEFT_EAR].x * img_w  #왼쪽 귀 x좌표 가져오기, 이미지 넓이를 곱해주는 이유는 x자표가 퍼센트로 가져오게 돼서 이미지의 가로길이를 곱해주는 것임 따라서 절대적인 수치가 나오게 됨.
        left_ear_y = landmark[mp_pose.PoseLandmark.LEFT_EAR].y * img_h  #왼족 귀 y좌표

        right_ear_x = landmark[mp_pose.PoseLandmark.RIGHT_EAR].x * img_w #오른쪽 귀 x
        right_ear_y = landmark[mp_pose.PoseLandmark.RIGHT_EAR].y * img_h #오른쪽 귀 y

        #귀의 중앙으로 얼굴 중심 가져오기
        center_x = int((left_ear_x + right_ear_x) / 2) 
        center_y = int((left_ear_y + right_ear_y) / 2)

        #반지름
        radius = int((left_ear_x - right_ear_x) / 2)
        radius = max(radius, 20) #반지름이 20보다 작으면 분석에 부정확할 수 있음으로 최솟값을 20으로 지정

        #어드레스(스윙의 시작 지점)시의 즉,  첫 프레임에서만 실행되는 코드
        if is_first: # 어드레스 시 첫 프레임의 머리 좌표 저장
            first_center_x = center_x
            first_center_y = center_y
            first_radius = int(radius * 2)

            is_first = False
        
        #첫 스윙 이후에 계속 수행
        #img_result : 도형 및 랜드마크가 그려진 이미지
        else:
            #img_result에 첫번째 프레임 머리의 중심좌표와 반지름을 사용해서 노란색(0,255,255)의 원을 2만큼의 선의 두깨로 원 그리기
            #직사각형 pt1 : 왼쪽 위 점, pt2 : 오른쪽 아래 점
            #cv2.rectangle(img_result, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 255), thickness=2)

            cv2.circle(img_result, center=(first_center_x, first_center_y),
                radius=first_radius, color=(0, 255, 255), thickness=2)
            

            color = (0, 255, 0) # 초록색

            # 머리가 원래 위치보다 많이 벗어난 경우 - > 작은원 빨간색으로 바꿈
            #왼쪽 항 : 작은 원의 왼쪽에서부터 거리
            #오른쪽 항 : 큰 원의 왼족에서 부터 거리
            if center_x - radius < first_center_x - first_radius \
                or center_x + radius > first_center_x + first_radius:
                color = (0, 0, 255) # 빨간색

            #벗어나면 빨강, 안 벗어나면 초록인 원을 현재 프레임에 draw
            cv2.circle(img_result, center=(center_x, center_y),
                radius=radius, color=color, thickness=2)

    cv2.imshow('AI Golf Coach', img_result) #이미지를 화면에 표시
    out.write(img_result)                   #이미지를 out 동영상 캡처 객체에 프레임 쓰기

    if cv2.waitKey(1) == ord('q'):
        break

pose.close()    #모델 객체 닫기
cap.release()   #비디오 캡처 객체 해제, 웹캠 연결 해제
out.release()   #쓰기 객체 닫기
