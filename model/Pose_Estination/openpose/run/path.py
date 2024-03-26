from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
protoFile = str(BASE_DIR)+"\\models\\pose\\body_25\\pose_deploy.prototxt"

weightsFile = str(BASE_DIR)+"\\models\\pose\\body_25\\pose_iter_584000.caffemodel"


print(protoFile)
print(weightsFile)