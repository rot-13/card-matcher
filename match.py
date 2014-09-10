import numpy as np
import cv2
import pickle
import sys
import time
from matplotlib import pyplot as plt

import os.path

img2 = cv2.imread('photo2.jpg',0) # trainImage

# Initiate SIFT detector
sift = cv2.SURF()
sift.upright = 1
sift.hessianThreshold = 200

kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_LINEAR = 0
FLANN_INDEX_KDTREE = 1
FLANN_INDEX_KMEANS = 2
FLANN_INDEX_COMPOSITE = 3
FLANN_INDEX_KDTREE_SINGLE = 4
FLANN_INDEX_HIERARCHICAL = 5
FLANN_INDEX_LSH = 6
FLANN_INDEX_SAVED = 254
FLANN_INDEX_AUTOTUNED = 255

FLANN_CENTERS_RANDOM = 0
FLANN_CENTERS_GONZALES = 1
FLANN_CENTERS_KMEANSPP = 2
FLANN_CENTERS_GROUPWISE = 3

#index_params = dict(algorithm = FLANN_INDEX_AUTOTUNED, target_precision = 0.1, sample_fraction = 0.1)
#index_params = dict(algorithm = FLANN_INDEX_COMPOSITE, branching = 4, iterations = 1, trees = 1)
#index_params = dict(algorithm = FLANN_INDEX_COMPOSITE, branching = 4, iterations = 1, trees = 1)
#index_params = dict(algorithm = FLANN_INDEX_KMEANS, branching = 4, iterations = 1)
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 1)
#index_params= dict(algorithm = FLANN_INDEX_LSH,
                   #table_number = 1, # 12
                   #key_size = 10,     # 20
                   #multi_probe_level = 0) #2
search_params = dict(checks=5)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

if os.path.exists('./cards.db'):
  dbFile = open('./cards.db', 'r')
  images = pickle.load(dbFile)
  dbFile.close()
else:
  images = []
  for filename in os.listdir('./two_cards/'):
    if not filename.endswith(".png"):
      continue
    img1 = cv2.imread('cards/' + filename,0)  # queryImage

    # find the keypoints and descriptors with SIFT
    print 'Detecting... ', filename
    kp1, des1 = sift.detectAndCompute(img1,None)
    images.append({'filename': filename, 'descriptor': des1 })
  dbFile = open('./cards.db', 'w')
  pickle.dump(images, dbFile)
  dbFile.close()

start = time.clock()
for img in images:
  print 'Matching...'
  matches = flann.knnMatch(img['descriptor'],des2,k=2)

  print 'filtering...'
  goodMatches = 0
  # ratio test as per Lowe's paper
  for i,pair in enumerate(matches):
    if len(pair) >= 2:
        if pair[0].distance < 0.7*pair[1].distance:
            goodMatches += 1
  print img['filename'], goodMatches
end = time.clock()
print end - start
  #draw_params = dict(matchColor = (0,255,0),
                    #singlePointColor = (255,0,0),
                    #matchesMask = matchesMask,
                    #flags = 0)
  #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

  #plt.imshow(img3,),plt.show()
