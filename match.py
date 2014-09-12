import time
import cv2, cv
import pickle
import sys
import os.path
from operator import itemgetter

# Initiate SIFT detector
sift = cv2.SIFT()

def png_to_grayscale_and_mask(img):
  if len(img.shape) > 2 and img.shape[2] > 3:
    mask = img[:,:,3]
  else:
    mask = None
  color = img[:,:,range(0,3)]
  grayscale = cv2.cvtColor(color, cv.CV_BGR2GRAY)
  return (grayscale, mask)

# first parameter is a list of image file names
# second parameter is the path to the db file
def load_images_descriptors(imagesList, images_db_path):
    images = []
    if os.path.exists(images_db_path):
        db_file = open(images_db_path, 'r')
        images = pickle.load(db_file)
        db_file.close()
    else:
        for filename in imagesList:
            if not filename.endswith(".png"):
                continue
            current_image = cv2.imread(filename,-1)  # queryImage
            grayscale, mask = png_to_grayscale_and_mask(current_image)

            # find the keypoints and descriptors with SIFT
            print 'Detecting... ', filename
            kp1, des1 = sift.detectAndCompute(grayscale, None)
            matchImg = cv2.drawKeypoints(grayscale, kp1)
            images.append({'filename': filename, 'descriptor': des1 })
        db_file = open(images_db_path, 'w')
        pickle.dump(images, db_file)
        db_file.close()
    return images

def descriptors_for_input_image(img_to_match, resize_factor=0.25):
    img_to_match = cv2.resize(img_to_match, (0,0), fx=resize_factor, fy=resize_factor) #we need to scale it down to a low res
    kp2, des2 = sift.detectAndCompute(img_to_match, None)
    return des2

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
search_params = dict(checks=5)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)

def find_match(input_descriptors, images, top = 3):
    imgMatches = []
    for img in images:
        matches = flann.knnMatch(img['descriptor'], input_descriptors, k=2)

        goodMatches = 0
        # ratio test as per Lowe's paper
        for i,pair in enumerate(matches):
            if len(pair) >= 2:
                if pair[0].distance < 0.7*pair[1].distance:
                    goodMatches += 1
        imgMatches.append((img['filename'], goodMatches))

    imgMatches = sorted(imgMatches, key = itemgetter(1), reverse=True)
    return imgMatches[:top]

def main():
  ####
  # argv[1]: card to find a match for.
  # argv[2]: path to cards to match against.
  ####
  card_to_match_path = sys.argv[1]
  current_path = sys.argv[2]

  images_db_path = current_path + '/images.db'
  image_filenames = [os.path.join(current_path, fileName) for fileName in os.listdir(current_path)]
  images = load_images_descriptors(image_filenames, images_db_path)
  start = time.clock()
  find_match(card_to_match_path, images)
  end = time.clock()
  print end - start

if __name__ == "__main__":
  main()
