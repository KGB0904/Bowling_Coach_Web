import cv2 as cv
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
#print(BASE_DIR)
path=str(BASE_DIR)+"\\graph.opt.pb"
#print("!!!!!!!",path)
#net =cv.dnn.readNetFromTensorflow(path)
net = cv.dnn.readNetFromTensorflow("C:/Users/dongj/Desktop/Bowling_Coach/openpose2/human-pose-estimation-opencv-master/graph_opt.pb")


inWidth = 368
inHeight = 368
thr = 0.2

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                   "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                   "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                   "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                   ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                   ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                   ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                   ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

img=cv.imread("C:\\Users\\dongj\\Desktop\\Bowling_Coach\\openpose2\\human-pose-estimation-opencv-master\\image.jpg")
plt.imshow(img)