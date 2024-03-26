#수정예정 검색해서 코드 가져다 쓰기


import cv2
import mediapipe as mp

#미디어파이프의 Pose 모델 라이브러리 

#랜드마크(관절포인트) 이미지에 그리기
mp_drawing = mp.solutions.drawing_utils

#랜드마크 표시하는 방법 즉, 그려지는 스타일 결정
mp_drawing_styles = mp.solutions.drawing_styles

#미디어파이프 포즈 제공, 포즈 추정 : 사용자가 어떤 포즈를 취하는지.
mp_pose = mp.solutions.pose

#비디오 경로
video_path = '..\\data\\golf.mp4'

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


    img_result = img.copy()     #원본 이미지 복사

    cv2.imshow('AI Golf Coach', img_result) #이미지를 화면에 표시
    out.write(img_result)                   #이미지를 out 동영상 캡처 객체에 프레임 쓰기

    if cv2.waitKey(1) == ord('q'):
        break

pose.close()    #모델 객체 닫기
cap.release()   #비디오 캡처 객체 해제, 웹캠 연결 해제
out.release()   #쓰기 객체 닫기
