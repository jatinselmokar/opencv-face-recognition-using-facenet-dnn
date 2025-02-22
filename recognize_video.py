# USAGE
# python recognize_video.py --detector face_detection_model \
#	--embedding-model openface_nn4.small2.v1.t7 \
#	--recognizer output/recognizer.pickle \
#	--le output/le.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import numpy as np

def who_is_it(vector,database_encode):
	encoding = vector
	min_dist = 100

	for i in range(len(database["embeddings"])):
		db_enc = database["embeddings"][i]
		name = database["names"][i]
		dist = np.linalg.norm(encoding - db_enc)

		if dist < min_dist:
			min_dist = dist
			identity = name
	if not min_dist < 0.55:
		identity = "Not in database"
	print(min_dist)
	return min_dist, identity

#File paths
filedir = os.path.dirname(os.path.realpath(__file__))
detector_path = os.path.join(filedir, "face_detection_model")
embedding_model_path = os.path.join(filedir, "openface_nn4.small2.v1.t7")
model = os.path.join(filedir, "output", "model.pickle")
label_encoder =os.path.join(filedir, "output", "label_encoder.pickle")
model = os.path.join(filedir, "output", "embeddings.pickle")
confidence_limit = 0.80

database = pickle.loads(open(model, "rb").read())

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.join(detector_path, "deploy.prototxt")
modelPath = os.path.join(detector_path,	"res10_300x300_ssd_iter_140000.caffemodel")
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(embedding_model_path)

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(model, "rb").read())
le = pickle.loads(open(label_encoder, "rb").read())

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
time.sleep(2.0)

# start the FPS throughput estimator
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	_,frame = capture.read()

	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]

	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)

	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > confidence_limit:
			# compute the (x, y)-coordinates of the bounding box for
			# the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI
			face = frame[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]

			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

			# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()

			similarity, name = who_is_it(vec, database)
			# perform classification to recognize the face
			# preds = recognizer.predict_proba(vec)[0]
			# j = np.argmax(preds)
			# proba = preds[j]
			# name = le.classes_[j]

			# draw the bounding box of the face along with the
			# associated probability
			text = "{}: {:.2f}".format(name, similarity)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	# update the FPS counter
	fps.update()

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
capture.release()
cv2.destroyAllWindows()
