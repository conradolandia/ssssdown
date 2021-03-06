#! /usr/bin/python 

from tqdm import tqdm
import requests
from clint.textui import progress
import os
import glob

path = 'ssss'
os.makedirs(path, exist_ok=True)
files = glob.glob(path + '/*.jpg')
comicCounter = len(files)  # reads the number of files in the folder to start downloading at the next comic
print(str(comicCounter) + " files currently in the folder.")
errors = 0

def download_comic(url,comicName):
  image = requests.get(url, stream=True)
  total_length = int(image.headers.get('content-length'))
  file_type = image.headers.get('content-type')
  status_code = image.status_code

  if status_code == 200 and total_length > 0 and file_type == 'image/jpeg':
    print('---') 
    print(comicName + ": Downloading...")
    with open(comicName, 'wb') as f:
      for chunk in progress.bar(image.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        if chunk:
          f.write(chunk)
          f.flush()
    print(comicName + ": Ready.")
    os.rename(comicName, path + '/' + comicName)

  else:
    print(str("comic" + ' ' + str(comicCounter) + ' ' + "does not exist"))
    print("all comics are up to date")
    global errors
    errors += 1

while errors == 0:
  comicCounter += 1
  comicNumber = comicCounter
  comicName = str(comicNumber) + ".jpg"
  url = str("http://www.sssscomic.com/comicpages/" + comicName)  
  download_comic(url,comicName) 
