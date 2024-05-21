#!/usr/bin/env python
# coding: utf-8
import os,time
import sys
import numpy as np
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv1D, Flatten, TimeDistributed

from get_folder import * 

start_time = time.time()    #피드백 걸린 시간 측정

file_path = os.path.abspath(__file__)
dir = os.path.dirname(file_path)
#print("Current running model.py path",dir,flush=True)

output_folder=get_next_output_folder(dir)

#output_folder = os.path.join(dir, "output_frame")



if len(sys.argv) != 2:
    video_path='C:\\Users\\428-3090\\Desktop\\BFP\\Data_Sample\\bowling_1.MP4'
    #print("Error! : Usage: python your_script.py <video_path>", flush=True)
    #exit(1)
else:
    video_path = sys.argv[1]


print("CheckPoint 1 : Start feedback",flush=True)

#video_path='C:\\Users\\428-3090\\Desktop\\BFP\\Data_Sample\\bowling_1.MP4'

def count_frames(video_path):
    if not os.path.isfile(video_path):
        print(f"Error! : Warning: '{video_path}' file does not exist.", flush=True)
        return None
    
    # Open the video and return the total number of frames
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.release()  # Release resources
    return total_frames

# Example usage
frame_count = count_frames(video_path)
#if frame_count is not None:
    #print(f"Total frames in the video: {frame_count}")


def split_video_into_frames(video_path, output_folder, num_frames=60):
    # Load the video and get the total number of frames
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    #print(total_frames)
    
    # Calculate the interval for selecting frames with uniform spacing
    interval = total_frames // num_frames
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Save selected frames as image files
    saved_frames = 0
    for i in range(num_frames):
        frame_pos = i * interval
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        
        success, frame = video.read()
        if not success:
            break
        
        cv2.imwrite(f"{output_folder}/frame_{i+1:03d}.jpg", frame)
        saved_frames += 1
    
    video.release()
    
    # Print a message if the number of saved frames is not 60
    if saved_frames != num_frames:
        print("Error! Not 60 frames")
    else:
        pass


    
split_video_into_frames(video_path, output_folder, 60)

print("CheckPoint 2 : Successfully split into 60 frames", flush=True)
#print("CheckPoint 1 : Start processing VIDEO to receive feedback ",flush=True)






# Load the MoveNet model
movenet_model = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
movenet=movenet_model.signatures['serving_default']

def load_and_preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize_with_pad(image, 192, 192)
    image = tf.expand_dims(image, axis=0)
    image = tf.cast(image, dtype=tf.int32)
    return image

def get_keypoints(image_path):
    image = load_and_preprocess_image(image_path)
    keypoints = movenet(image)['output_0']
    keypoints = tf.squeeze(keypoints, axis=0)
    return keypoints.numpy().flatten()

base_dir = output_folder

sequences = []

sequence_keypoints = []

for i in range(1, 61):
    frame_filename = f'frame_{i:03d}.jpg'
    image_path = os.path.join(base_dir, frame_filename)
    keypoints = get_keypoints(image_path)
    sequence_keypoints.append(keypoints)
    
sequences.append(sequence_keypoints)

sequences = np.array(sequences)

sequences_list = sequences.tolist()

# Save as JSON file
data = {'sequences': sequences_list}
with open('unlabeled_data.json', 'w') as json_file:
    json.dump(data, json_file)

print("CheckPoint 3 : Sequence Data Extracted Successfully", flush=True)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Conv1D, Flatten, TimeDistributed

model_path=os.path.join(dir, "h5","CNN_LSTM_V1.h5")
model = tf.keras.models.load_model(model_path)
model.summary()


with open('unlabeled_data.json', 'r') as file:
    data = json.load(file)
    sequences = np.array(data['sequences'])

    test_x_train = []
    test_y_train = []

    window_size = 5  # Predict the next frame using 5 previous frames

    # Extract sequences from the data
    for sequence in sequences:
        # Extract all possible windows within each sequence
        for i in range(len(sequence) - window_size):
            test_x_train.append(sequence[i:i+window_size])
            test_y_train.append(sequence[i+window_size])

    # Convert to numpy arrays
    test_x_train = np.array(test_x_train)
    test_y_train = np.array(test_y_train)

    # Print data shapes
    #print("test_x_train shape:", test_x_train.shape)
    #print("test_y_train shape:", test_y_train.shape)


# Perform predictions
predictions = model.predict(test_x_train)
def detect_anomalies(real, predicted, threshold=0.33):
    # Calculate the difference between real and predicted values
    diff = np.linalg.norm(real - predicted, axis=1)
    anomalies = diff > threshold
    return anomalies, diff


# Detect anomalies
anomalies, differences = detect_anomalies(test_y_train, predictions)
print("CheckPoint 4 : prediction success", flush=True)
#print(anomalies)
#print(differences)

#idx = 6
#for i in anomalies:
#    if i == False:
#        print("Frame",idx,"is False")
#    idx += 1
def check_posture(true_array):
    # True 값의 비율 계산
    true_percentage = int(sum(true_array) / len(true_array) * 100)
    

    # 정확도 계산
    accuracy = round(true_percentage, 2)

        # Returning messages based on conditions
    if true_percentage >= 95:
        return f"This is the correct posture. Posture Accuracy: {accuracy}%"
    elif 80 <= true_percentage < 95:
        return f"This is a decent posture. Posture Accuracy: {accuracy}%"
    elif 60 <= true_percentage < 80:
        return f"This is a disappointing posture. Posture Accuracy: {accuracy}%"
    else:
        return f"This is a wrong posture. Posture Accuracy: {accuracy}%"

    
result = check_posture(anomalies)
print(result, flush=True)


#피드백 걸린 총 시간 측정
end_time = time.time()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)

print(f"FeedBack Time {int(minutes)}:{seconds:.2f}", flush=True)

