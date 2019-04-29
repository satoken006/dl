# -*- Coding: utf-8 -*-

class RepositoryParser:
    def __init__(self):
        print()

    def get_author_list(self, soup):
        titleElem = soup.find("h1")
        title = titleElem.get_text()
        print(title)
        divElem = titleElem.parent
        a_list = divElem.find_all("a")
        
        return a_list