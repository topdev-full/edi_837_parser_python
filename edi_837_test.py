import sys
import os
from edi_837 import parse_837

if __name__ == '__main__':
  base_dir = "F:/data/837_Raw/"
  for file_name in os.listdir(base_dir):
    # print(file_name)
    print(file_name)
    cnt1 = parse_837(base_dir+file_name)
    with open(base_dir+file_name, "r") as file1:
      read_content = file1.read()
      cnt2 = read_content.count("CLM")
      if cnt1 != cnt2:
        print(file_name, cnt1, cnt2)