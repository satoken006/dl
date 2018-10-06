import urllib.request, urllib.error
from bs4 import BeautifulSoup

html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/1")

soup = BeautifulSoup(html)
print( soup )