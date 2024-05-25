import random, time, os
print("CheckPoint 1 : Start feedback",flush=True)
time.sleep(1)
print("CheckPoint 2 : Successfully split into 60 frames", flush=True)

time.sleep(1)
print("CheckPoint 3 : Sequence Data Extracted Successfully", flush=True)

time.sleep(1)
print("CheckPoint 4 : prediction success", flush=True)


file_path = os.path.abspath(__file__)
dir = os.path.dirname(file_path)

#gif_path 저장되는 폴더
gif_output_folder = os.path.abspath(os.path.join(dir, "..", "..","server","FBHtml","gif"))

#경보가 만들어줄꺼임
gif_path=os.path.join(gif_output_folder, "output.gif")


print(f"gif_path:{gif_path}",flush=True)


true_percentage = 80#random.randint(1,100)
accuracy=true_percentage
# Returning messages based on conditions
if true_percentage >= 95:
    print(f"This is the correct posture. Accuracy: {accuracy}%",flush=True)
elif 80 <= true_percentage < 95:
    print(f"This is a decent posture. Accuracy: {accuracy}%",flush=True)
elif 50 <= true_percentage < 80:
    print(f"This is not a good posture. Accuracy: {accuracy}%",flush=True)
else:
    print(f"This is a wrong posture. Accuracy: {accuracy}%",flush=True)

time.sleep(1)

