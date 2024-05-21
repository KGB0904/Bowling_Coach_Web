#path code

import os
file_path = os.path.abspath(__file__)
dir = os.path.dirname(file_path)

print(dir)