import cv2
from pathlib import Path

# MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                "Background": 15 }

POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]
    
# BASE_DIR = openpose 폴더
BASE_DIR=Path(__file__).resolve().parent.parent

#prototxt
protoFile = str(BASE_DIR)+"\\models\\pose\\body_25\\pose_deploy.prototxt"
#coffemodel
weightsFile = str(BASE_DIR)+"\\models\\pose\\body_25\\pose_iter_584000.caffemodel"

# 위의 path에 있는 network 모델 불러오기
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# 입력 및 출력 비디오 파일 경로 설정
input_video_path = '01.mp4'  # 입력 비디오 파일 경로
output_video_path = 'output.mp4'  # 출력 비디오 파일 경로

# 입력 비디오 캡처
capture = cv2.VideoCapture(input_video_path)

# 출력 비디오 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_fps = capture.get(cv2.CAP_PROP_FPS)
output_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
output_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
output = cv2.VideoWriter(output_video_path, fourcc, output_fps, (output_width, output_height))

# 프레임 처리
while cv2.waitKey(1) < 0:
    has_frame, frame = capture.read()

    if not has_frame:
        break

    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    # 입력 이미지로부터 blob 생성
    input_width = 368
    input_height = 368
    input_scale = 1.0 / 255
    inp_blob = cv2.dnn.blobFromImage(frame, input_scale, (input_width, input_height), (0, 0, 0), swapRB=False, crop=False)

    # 네트워크에 전달
    net.setInput(inp_blob)

    # 결과 가져오기
    output = net.forward()

    # 포인트 초기화
    points = []

    # 키포인트 검출 및 표시
    for i in range(0, 15):
        prob_map = output[0, i, :, :]

        # 최대값 찾기
        _, prob, _, point = cv2.minMaxLoc(prob_map)

        # 원래 이미지 크기에 맞게 포인트 위치 조정
        x = int((frame_width * point[0]) / output.shape[3])
        y = int((frame_height * point[1]) / output.shape[2])

        # 신뢰도가 일정 값 이상인 경우에만 포인트 추가
        if prob > 0.1:
            points.append((x, y))
        else:
            points.append(None)

    # POSE_PAIRS에 따라 선 연결
    for pair in POSE_PAIRS:
        part_a = pair[0]
        part_a = BODY_PARTS[part_a]
        part_b = pair[1]
        part_b = BODY_PARTS[part_b]

        if points[part_a] and points[part_b]:
            cv2.line(frame, points[part_a], points[part_b], (0, 255, 0), 2)

    # 프레임 저장
    output.write(frame)

# 종료
capture.release()
output.release()
cv2.destroyAllWindows()
