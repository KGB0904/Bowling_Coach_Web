import cv2

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        cv2.imshow("test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()


# 모듈 불러오기: import 모듈 이름 - 이미지 사용을 위한 opencv,
# 이미지 저장 파일명 사용을 위한 datetime

#qimport cv2
#import datetime

#video_capture = cv2.VideoCapture(0)

#while (True):

#    grabbed, frame = video_capture.read()
#    cv2.imshow('Original Video', frame)

 #   key = cv2.waitKey(1);
 #   if key == ord('q'):
 #       break
 #   elif key == ord('s'):
 #       file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f") + '.jpg'
 #       cv2.imwrite(file, frame)
 #       print(file, ' saved')

#video_capture.release()
#cv2.destroyAllWindows()