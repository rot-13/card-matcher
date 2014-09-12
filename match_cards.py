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
  for imgMatch in match.find_match(input_descriptors, template_descriptors, top=2):
    print 'Matching ', os.path.dirname(imgMatch[0]), '...'
    cluster_dir = os.path.dirname(imgMatch[0])
    cluster_files = glob.glob(os.path.join(cluster_dir, '*.png'))
    cluster_files = [f for f in cluster_files if not f.endswith('template.png')]
    
    cluster_descriptors = match.load_images_descriptors(cluster_files, os.path.join(cluster_dir, 'images.db'))
    allMatches += match.find_match(input_descriptors, cluster_descriptors)

  allMatches = sorted(allMatches, key = itemgetter(1), reverse=True)

  print allMatches[0]

def main():
  find_cluster(sys.argv[1])

if __name__ == "__main__":
  main()
