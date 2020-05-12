import os
print(os.listdir(os.path.dirname(__file__)))

# import os
#
# print('getcwd:      ', os.getcwd())
# print('__file__:    ', os.path.dirname(__file__))
#
# filedir = os.path.dirname(os.path.realpath(__file__))
# detector_path = os.path.join(filedir, 'face_detection_model')
# # embedding_model_path = os.path.join(filedir, "extract_embeddings.py")
#
# print(filedir)
# print(detector_path)
# print(embedding_model_path)
# import sys
# import argparse
#
# ap = argparse.ArgumentParser()
# ap.add_argument('--b', default = "default", action="store", dest="bed")
# print(ap.parse_args().bed)
#
# # print(args.b)
# # def hello(a,b):
# #     print ('hello and thats your sum:')
# #     sum=float(a)+float(b)
# #     print (sum)
# #
# # if __name__ == "__main__":
# #     print("arg - ", sys.argv[0])
# #     # hello(sys.argv[1], sys.argv[2])
