import requests
from typing import List


__TARGET_URL = 'https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt'

__blacklist: List[str] = []


def load_blacklist() -> None:
    global __blacklist
    response = requests.get(__TARGET_URL, allow_redirects=True)
    __blacklist = [word for word in response.text.split('\n')]
    

def get_blacklist() -> List[str]:
  if __blacklist is None:
      raise Exception("Expensive model not loaded")
  return __blacklist
