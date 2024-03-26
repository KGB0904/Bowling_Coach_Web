import cv2
import mediapipe as mp
import numpy as np
import requests
import threading

PHONE_IP_ADDRESS = 'YOUR_PHONE_IP_ADDRESS'  # 핸드폰의 IP 주소 입력

def receive_frames():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        process_frame(frame)
    cap.release()

def process_frame(frame):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # To improve performance, optionally mark the image as not writeable to pass by reference
    frame_rgb.flags.writeable = False
    
    # Process the frame
    results = pose.process(frame_rgb)
    
    # Draw the pose landmarks on the image
    if results.pose_landmarks:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # Convert the RGB image back to BGR
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Show the frame
    cv2.imshow('Pose Detection', frame_bgr)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit()

# Start a separate thread to receive frames from the phone
thread = threading.Thread(target=receive_frames)
thread.start()
