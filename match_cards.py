import glob
import match
import sys

def find_cluster(img):
  template_files = glob.glob('./clusters/*/*/011*.png')
  template_descriptors = match.load_images_descriptors(template_files, './templates.db')
  match.find_match(img, template_descriptors)

def main():
  find_cluster(sys.argv[1])

if __name__ == "__main__":
  main()
