import glob
import match
import sys
import os
import cv2
import json
from time import time
from operator import itemgetter
from multiprocessing import Pool
from functools import partial

def average_image(paths):
  total_img = (cv2.imread(paths[0], 1) / 255.0)
  for i in range(1, len(paths)):
    total_img += (cv2.imread(paths[i], 1)/255.0)

  return (total_img / (len(paths)))*255.0


def get_template_image(dirpath):
  template_file = os.path.join(dirpath, 'template.png')
  if not os.path.exists(template_file):
    avg_img = average_image(glob.glob(os.path.join(dirpath, '?????.png')))
    cv2.imshow('zomg', avg_img)
    cv2.imwrite(template_file, avg_img)
  return template_file


def load_clusters_template_descriptors():
  template_dirs = glob.glob('./clusters/*/*/')
  template_files = map(get_template_image, template_dirs)
  template_files = [f for f in template_files if os.stat(f).st_size > 0]
  return match.load_images_descriptors(template_files, './templates.db')

def find_matches_in_clusters(input_descriptors, cluster_matches, num_of_processors=4):
    clusters_tuples = [(c, input_descriptors) for c in cluster_matches]
    if num_of_processors > 1:
        p = Pool(num_of_processors)
        allMatches = p.map(find_matches_in_cluster, clusters_tuples)
    else:
        allMatches = map(find_matches_in_cluster, clusters_tuples)
    allMatches = reduce(lambda x, y: x+y, allMatches)
    return sorted(allMatches, key = itemgetter(1), reverse=True)

def find_card_in_clusters(img, resize_factor=0.25):
  alls = time()
  start = time()
  print 'Loading clusters descriptors...'
  template_descriptors = load_clusters_template_descriptors()
  print 'Loaded clusters in:', time() - start, 'seconds'
  start = time()
  print 'Loading input image descriptors...'
  input_descriptors = match.descriptors_for_input_image(img, resize_factor)
  print 'Loaded input image in:', time() - start, 'seconds'
  print 'Searching for top clusters...'
  start = time()
  cluster_matches = match.find_match(input_descriptors, template_descriptors, top=4)
  print 'Found top clusters in:', time() - start, 'seconds'
  start = time()
  print 'Searching for image in top clusters...'
  matches = find_matches_in_clusters(input_descriptors, cluster_matches, num_of_processors=4)
  print 'Found match in:', time() - start, 'seconds with score:', matches[0][1]
  print 'Total time:', time() - alls, 'seconds'

  return matches[0]

def find_matches_in_cluster(cluster_and_descriptor):
    cluster, input_descriptors = cluster_and_descriptor
    imgMatch = cluster[0]
    print 'Matching ', os.path.dirname(imgMatch), '...'
    cluster_dir = os.path.dirname(imgMatch)
    cluster_files = glob.glob(os.path.join(cluster_dir, '*.png'))
    cluster_files = [f for f in cluster_files if not f.endswith('template.png')]

    cluster_descriptors = match.load_images_descriptors(cluster_files, os.path.join(cluster_dir, 'images.db'))
    return match.find_match(input_descriptors, cluster_descriptors)

def card_title(path):
  card_code = os.path.basename(path).split('.')[0]
  with open('cards.json') as data_file:
    cards = json.load(data_file)
    card = [c for c in cards if c["code"] == card_code]
    return card[0]["title"]

def main():
  img = cv2.imread(sys.argv[1], 0)
  card_file_name = find_card_in_clusters(img)[0]

if __name__ == "__main__":
  main()
