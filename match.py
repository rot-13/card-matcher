import time
import cv2
import pickle
import sys
import os.path

# Initiate SIFT detector
sift = cv2.SIFT()

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
            current_image = cv2.imread(filename,0)  # queryImage

            # find the keypoints and descriptors with SIFT
            print 'Detecting... ', filename
            kp1, des1 = sift.detectAndCompute(current_image, None)
            images.append({'filename': filename, 'descriptor': des1 })
        db_file = open(images_db_path, 'w')
        pickle.dump(images, db_file)
        db_file.close()
    return images

def find_match(img_to_match_path, images):
    img_to_match = cv2.imread(img_to_match_path, 0) # trainImage
    img_to_match = cv2.resize(img_to_match, (0,0), fx=0.10, fy=0.10) #we need to scale it down to a low res
    kp2, des2 = sift.detectAndCompute(img_to_match, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
    search_params = dict(checks=5)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)
    for img in images:
        print 'Matching...'
        matches = flann.knnMatch(img['descriptor'], des2, k=2)

        print 'Filtering...'
        goodMatches = 0
        # ratio test as per Lowe's paper
        for i,pair in enumerate(matches):
            if len(pair) >= 2:
                if pair[0].distance < 0.7*pair[1].distance:
                    goodMatches += 1
        print img['filename'], goodMatches

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
