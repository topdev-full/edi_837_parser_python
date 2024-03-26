import sys
import os
from edi_835 import parse_835

if __name__ == '__main__':
  base_dir = "F:/data/835_Raw/"
  for file_name in os.listdir(base_dir):
    # print(file_name)
    cnt1 = parse_835(base_dir+file_name)
    with open(base_dir+file_name, "r") as file1:
      read_content = file1.read()
      cnt2 = read_content.count("CLP*")
      if cnt1 != cnt2:
        print(file_name, cnt1, cnt2)
        # break