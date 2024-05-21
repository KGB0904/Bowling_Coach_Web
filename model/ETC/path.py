#path code

import os
file_path = os.path.abspath(__file__)
dir = os.path.dirname(file_path)
join_path=os.path.join(dir,"join_path")
print (join_path)

print(dir)