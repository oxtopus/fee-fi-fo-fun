from collections import defaultdict
import re
alnum = re.compile(r"\W+")
words = defaultdict(int)
skip = set(["to", "he", "and", "the", ""])
with open("20748.txt") as inp:
  inp.seek(131072)
  count = 0
  prev_line = ""
  while True:
    line = inp.readline()
    for line in line.split(" "):
      token = alnum.sub("", line).lower()
      if token not in skip:
        print token
    if inp.tell() >= 138922:
      break
