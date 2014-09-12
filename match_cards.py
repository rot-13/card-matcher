import glob
import match
import sys
import os

def find_cluster(img):
  template_files = glob.glob('./clusters/*/*/template.png')
  template_files = [f for f in template_files if os.stat(f).st_size > 0]
  template_descriptors = match.load_images_descriptors(template_files, './templates.db')
  print match.find_match(img, template_descriptors)

def main():
  find_cluster(sys.argv[1])

if __name__ == "__main__":
  main()
