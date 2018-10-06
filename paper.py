import urllib.request, urllib.error
from bs4 import BeautifulSoup

for i in range(1,107):
    try:
        html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/"+str(i))
    except urllib.error.HTTPError as e:
        continue

    soup = BeautifulSoup(html)
    print( soup )

    title = soup.find("h1").get_text()
    print( title )
    print()

    div = soup.find("div")
    div2 = div.find_all("div")[1]
    div3 = div2.find("div") # _2cXX...
    div4 = div3.find_all("div", recursive=False)[0]
    div5 = div4.find("div")
    header = div5.find("header")

    for a in header.find_all("a"):
        author = a.get_text(" ", strip=True)
        print(author)