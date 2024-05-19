import random, time
print("CheckPoint 1",flush=True)
time.sleep(1)
print("CheckPoint 2",flush=True)
time.sleep(1)
print("CheckPoint 3",flush=True)
time.sleep(1)

true_percentage = random.randint(1,100)
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