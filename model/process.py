import os
import sys
import numpy as np
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import json
from PIL import Image, ImageDraw
import imageio
from get_folder import * 

print("CheckPoint 1 : Start feedback")
movenet = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4").signatures['serving_default']
# Define keypoint dictionary and edge pairs
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

KEYPOINT_EDGE_INDS = [
    (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6), (5, 7), (7, 9),
    (6, 8), (8, 10), (5, 6), (5, 11), (6, 12), (11, 12), (11, 13), 
    (13, 15), (12, 14), (14, 16)
]

def _keypoints_and_edges_for_display(keypoints_with_scores, original_height, original_width, keypoint_threshold=0.11):
    keypoints_all = []
    keypoint_edges_all = []
    num_instances, _, _, _ = keypoints_with_scores.shape
    for idx in range(num_instances):
        kpts_x = keypoints_with_scores[0, idx, :, 1]
        kpts_y = keypoints_with_scores[0, idx, :, 0]
        kpts_scores = keypoints_with_scores[0, idx, :, 2]

        # Adjust keypoints to the original image size
        kpts_absolute_xy = np.stack([original_width * np.array(kpts_x), original_height * np.array(kpts_y)], axis=-1)
        keypoints_all.append(kpts_absolute_xy)

        for edge_pair in KEYPOINT_EDGE_INDS:
            if (kpts_scores[edge_pair[0]] > keypoint_threshold and kpts_scores[edge_pair[1]] > keypoint_threshold):
                x_start = kpts_absolute_xy[edge_pair[0], 0] 
                y_start = kpts_absolute_xy[edge_pair[0], 1]
                x_end = kpts_absolute_xy[edge_pair[1], 0] 
                y_end = kpts_absolute_xy[edge_pair[1], 1]
                line_seg = np.array([[x_start, y_start], [x_end, y_end]])
                keypoint_edges_all.append(line_seg)

    if keypoints_all:
        keypoints_xy = np.concatenate(keypoints_all, axis=0)
    else:
        keypoints_xy = np.zeros((0, 17, 2))

    if keypoint_edges_all:
        edges_xy = np.stack(keypoint_edges_all, axis=0)
    else:
        edges_xy = np.zeros((0, 2, 2))

    return keypoints_xy, edges_xy

def draw_keypoints(image, keypoints_with_scores, original_height, original_width, is_anomaly):
    height, width, _ = image.shape
    
    # Compute scaling factors
    scale_x = height / width
    scale_y = height / original_height
    
    # Central coordinates for original and new image sizes
    center_x_orig = original_width / 2
    center_y_orig = original_height / 2
    center_x_new = width / 2
    center_y_new = height / 2
    
    keypoint_locs, keypoint_edges = _keypoints_and_edges_for_display(keypoints_with_scores, original_height, original_width)
    color = (0, 255, 0) if is_anomaly else (0, 0, 255)  # Green for anomaly, Red for correct

    for edge in keypoint_edges:
        start_point, end_point = edge
        # Translate points to the center, scale, then translate back
        start_point = ((start_point[0] - center_x_orig) * scale_x + center_x_new, 
                       (start_point[1] - center_y_orig) * scale_y + center_y_new)
        end_point = ((end_point[0] - center_x_orig) * scale_x + center_x_new, 
                     (end_point[1] - center_y_orig) * scale_y + center_y_new)
        start_point = tuple(map(int, start_point))
        end_point = tuple(map(int, end_point))
        cv2.line(image, start_point, end_point, color=color, thickness=2)

    for keypoint in keypoint_locs:
        x, y = keypoint
        # Translate points to the center, scale, then translate back
        center = ((x - center_x_orig) * scale_x + center_x_new, 
                  (y - center_y_orig) * scale_y + center_y_new)
        center = tuple(map(int, center))
        cv2.circle(image, center, 3, color=color, thickness=-1)

    return image


# Load the MoveNet model

def load_and_preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)

    # Save the original size
    original_height = tf.shape(image)[0]
    original_width = tf.shape(image)[1]

    image = tf.image.resize_with_pad(image, 192, 192)
    image = tf.expand_dims(image, axis=0)
    image = tf.cast(image, dtype=tf.int32)
    return image, original_height, original_width

def get_keypoints(image_path):
    image, original_height, original_width = load_and_preprocess_image(image_path)
    keypoints = movenet(image)['output_0']
    return keypoints.numpy(), original_height.numpy(), original_width.numpy()

def detect_anomalies(real, predicted, threshold=0.33):
    diff = np.linalg.norm(real - predicted, axis=1)
    anomalies = diff > threshold
    return anomalies, diff

def split_video_into_frames(video_path, output_folder, num_frames=60):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_frames // num_frames
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
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
    if saved_frames != num_frames:
        print("Error ! : Not 60 frames",flush=True)
    else:
        print(f"Saved {num_frames} frames to {output_folder}",flush=True)

def main(video_path):
    root = os.path.dirname(os.getcwd())
    output_folder = os.path.join(root, "model", "output_folder")
    gif_output_path = os.path.join(root, "model", "output.gif")

    split_video_into_frames(video_path, output_folder, 60)
    print("CheckPoint 2 : 60프레임으로 분할 성공",flush=True)

    base_dir = output_folder
    sequences = []
    sequence_keypoints = []
    original_heights = []
    original_widths = []

    for i in range(1, 61):
        frame_filename = f'frame_{i:03d}.jpg'
        image_path = os.path.join(base_dir, frame_filename)
        keypoints, original_height, original_width = get_keypoints(image_path)
        sequence_keypoints.append(keypoints)
        original_heights.append(original_height)
        original_widths.append(original_width)

    sequences.append(sequence_keypoints)
    sequences = np.array(sequences)

    data = {'sequences': sequences.tolist()}
    with open('unlabeled_data.json', 'w') as json_file:
        json.dump(data, json_file)

    print("CheckPoint 2 : Sequence Data Extracted Successfully",flush=True)

    model = tf.keras.models.load_model('C:/Users/428-3090/Desktop/CNN_LSTM/asdf/VC_with_Model-main/VC_Linux/src/model/CNN_LSTM_V1.h5')
    model.summary()

    with open('unlabeled_data.json', 'r') as file:
        data = json.load(file)
        sequences = np.array(data['sequences'])

        test_x_train = []
        test_y_train = []

        window_size = 5
        for sequence in sequences:
            for i in range(len(sequence) - window_size):
                test_x_train.append(sequence[i:i+window_size])
                test_y_train.append(sequence[i+window_size])

        test_x_train = np.array(test_x_train)
        test_y_train = np.array(test_y_train)

    # Reshape the data to match the expected input shape of the model
    test_x_train = test_x_train.reshape((test_x_train.shape[0], window_size, 51, 1))
    test_y_train = test_y_train.reshape((test_y_train.shape[0], 51))

    predictions = model.predict(test_x_train)
    anomalies, differences = detect_anomalies(test_y_train, predictions)
    print("CheckPoint 3 : prediction success",flush=True)

    def check_posture(true_array):
        true_percentage = sum(true_array) / len(true_array) * 100
        accuracy = round(true_percentage, 2)
        if true_percentage >= 95:
            return f"This is the correct posture. Accuracy: {accuracy}%"
        elif 80 <= true_percentage < 95:
            return f"This is a decent posture. Accuracy: {accuracy}%"
        elif 50 <= true_percentage < 80:
            return f"This is not a good posture. Accuracy: {accuracy}%"
        else:
            return f"This is a wrong posture. Accuracy: {accuracy}%"

    result = check_posture(anomalies)
    print(result,flush=True)

    frames_with_keypoints = []
    for i in range(1, 61):
        frame_filename = f'frame_{i:03d}.jpg'
        image_path = os.path.join(base_dir, frame_filename)
        image = cv2.imread(image_path)
        keypoints = sequence_keypoints[i - 1].reshape((1, 1, 17, 3))
        original_height = original_heights[i - 1]
        original_width = original_widths[i - 1]
        
        if i <= 5:
            is_anomaly = False
        else:
            is_anomaly = anomalies[i - 5] if i - 5 < len(anomalies) else False
        
        frame_with_keypoints = draw_keypoints(image, keypoints, original_height, original_width, is_anomaly)
        frames_with_keypoints.append(cv2.cvtColor(frame_with_keypoints, cv2.COLOR_BGR2RGB))

        opt_path = os.path.join(base_dir, "/joint")
        cv2.imwrite(f"{opt_path}/frame_{i+1:03d}.jpg", frame_with_keypoints)
    # for i in range(1, 61):
    #     frame_filename = f'frame_{i:03d}.jpg'
    #     image_path = os.path.join(base_dir, frame_filename)
    #     image = cv2.imread(image_path)
    #     keypoints = sequence_keypoints[i - 1].reshape((1, 1, 17, 3))
    #     original_height = original_heights[i - 1]
    #     original_width = original_widths[i - 1]
    #     is_anomaly = anomalies[i - 1] if i - 1 < len(anomalies) else False
    #     frame_with_keypoints = draw_keypoints(image, keypoints, original_height, original_width, is_anomaly)
    #     frames_with_keypoints.append(cv2.cvtColor(frame_with_keypoints, cv2.COLOR_BGR2RGB))

    imageio.mimsave(gif_output_path, frames_with_keypoints, fps=6)
    print("CheckPoint 4 : GIF Generation Successfull", flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error ! : Usage: python your_script.py <video_path>",flush=True)
        sys.exit(1)
    file_path = os.path.abspath(__file__)
    dir = os.path.dirname(file_path)


    output_folder=get_next_output_folder(dir)
    video_path = sys.argv[1]
    main(video_path)
