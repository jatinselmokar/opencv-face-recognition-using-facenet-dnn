# USAGE
# python train_model.py --embeddings output/embeddings.pickle \
#	--recognizer output/recognizer.pickle --le output/le.pickle

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
import os

#File paths
filedir = os.path.dirname(os.path.realpath(__file__))
embeddings = os.path.join(filedir, "output", "embeddings.pickle" )
out_model = os.path.join(filedir, "output", "model.pickle")
out_label_encoder =os.path.join(filedir, "output", "label_encoder.pickle")

# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open(embeddings, "rb").read())

# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
recognizer = SVC(C=2, kernel="rbf", probability=True)
recognizer.fit(data["embeddings"], labels)

f = open(out_model, "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
f = open(out_label_encoder, "wb")
f.write(pickle.dumps(le))
f.close()
