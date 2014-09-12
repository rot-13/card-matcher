import glob
import match
import sys
import os
import cv2
import time

from operator import itemgetter

def find_cluster(img, resize_factor=0.25):
  alls = time.clock()
  start = time.clock()
  print 'Loading clusters descriptors...'
  template_files = glob.glob('./clusters/*/*/template.png')
  template_files = [f for f in template_files if os.stat(f).st_size > 0]
  template_descriptors = match.load_images_descriptors(template_files, './templates.db')
  print 'Loaded clusters in:', time.clock() - start, 'seconds'

  allMatches = []
  start = time.clock()
  print 'Loading input image descriptors...'
  input_descriptors = match.descriptors_for_input_image(img, resize_factor)
  print 'Loaded input image in:', time.clock() - start, 'seconds'
  print 'Searching for cluster...'
  start = time.clock()
  cluster_matches = match.find_match(input_descriptors, template_descriptors, top=2)
  print 'Found clusters in:', time.clock() - start, 'seconds'
  start = time.clock()
  print 'Searching for image in top clusters...'
  for imgMatch in cluster_matches:
    print 'Matching ', os.path.dirname(imgMatch[0]), '...'
    cluster_dir = os.path.dirname(imgMatch[0])
    cluster_files = glob.glob(os.path.join(cluster_dir, '*.png'))
    cluster_files = [f for f in cluster_files if not f.endswith('template.png')]

    cluster_descriptors = match.load_images_descriptors(cluster_files, os.path.join(cluster_dir, 'images.db'))
    allMatches += match.find_match(input_descriptors, cluster_descriptors)

  allMatches = sorted(allMatches, key = itemgetter(1), reverse=True)
  print 'Found match in:', time.clock() - start, 'seconds'
  print 'Total time:', time.clock() - alls, 'seconds'

  return allMatches[0]

def main():
  img = cv2.imread(sys.argv[1], 0)
  card_file_name = find_cluster(img)[0]

  print os.path.basename(card_file_name).split('.')[0]

if __name__ == "__main__":
  main()
