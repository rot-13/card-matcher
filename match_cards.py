import glob
import match
import sys
import os

from operator import itemgetter

def find_cluster(img):
  print 'Searching for cluster...'
  template_files = glob.glob('./clusters/*/*/template.png')
  template_files = [f for f in template_files if os.stat(f).st_size > 0]
  template_descriptors = match.load_images_descriptors(template_files, './templates.db')

  allMatches = []
  input_descriptors = match.descriptors_for_input_image(img)
  for imgMatch in match.find_match(input_descriptors, template_descriptors, top=4):
    print 'Matching ', os.path.dirname(imgMatch[0]), '...'
    cluster_dir = os.path.dirname(imgMatch[0])
    cluster_files = glob.glob(os.path.join(cluster_dir, '*.png'))
    cluster_files = [f for f in cluster_files if not f.endswith('template.png')]

    cluster_descriptors = match.load_images_descriptors(cluster_files, os.path.join(cluster_dir, 'images.db'))
    allMatches += match.find_match(input_descriptors, cluster_descriptors)

  allMatches = sorted(allMatches, key = itemgetter(1), reverse=True)

  return allMatches[0]

def main():
  img = cv2.imread(sys.argv[1], 0)
  card_file_name = find_cluster(img)[0]

  print os.path.basename(card_file_name).split('.')[0]

if __name__ == "__main__":
  main()
