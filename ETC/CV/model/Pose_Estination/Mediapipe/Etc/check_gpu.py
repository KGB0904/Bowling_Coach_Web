import GPUtil
from time import sleep



def check_gpu():
    GPUs = GPUtil.getGPUs()
    cnt=0
    sums=0
    
    for gpu in GPUs:
        print(f"GPU ID: {gpu.id}, Name: {gpu.name}, Load: {gpu.load*100}%, GPU Temp: {gpu.temperature} C")
        sums+=gpu.load*100
        cnt+=cnt+1

    return sums/cnt
            

        