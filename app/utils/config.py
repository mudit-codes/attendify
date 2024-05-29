import os

# path to capture faces
DATASET = "dataset"

# face encoding and attendance output path
ENCODINGS_PATH = "output/encodings.pickle"
ATTENDANCE_PATH = "output/attendance.csv"

# face detector model
PROTOTXT_PATH = "model/deploy.prototxt.txt"
MODEL_PATH = "model/res10_300x300_ssd_iter_140000.caffemodel"

# capture duration
# 5 * 60 * 1000 = 300000ms or 5 minutes
CAPTURE_DURATION = 90000