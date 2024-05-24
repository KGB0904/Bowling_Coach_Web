#path code

import os
#file_path = os.path.abspath(__file__)
#dir = os.path.dirname(file_path)
#join_path=os.path.join(dir,"join_path")
#print (join_path)

#print(dir)

root = os.path.dirname(os.getcwd())
output_folder = os.path.join(root, "model", "output_folder") #frame
gif_output_path = os.path.join(root, "model", "output.gif")  #gif

print(output_folder)
print(gif_output_path)