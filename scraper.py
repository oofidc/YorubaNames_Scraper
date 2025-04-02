from bs4 import BeautifulSoup as bs4
import requests
import re


yo_alphabet = ['a','b','d','e','ẹ','f','g','gb','h','i','j','k','l','m','n','o','ọ','p','r','s','ṣ','t','u','w','y']

#Returns the all names with the first character passed
def names_by_first_char(first_char):
    url = "https://www.yorubaname.com/alphabet/" + first_char
    page = requests.get(url=url).text
    #re.findall("<li>.*</li></a>",page)
    return [name.text for name in bs4(page,"html.parser").find('div',class_='alphabet-listing').find_all('li')]
#Returns all names
def get_all_names():
    names = []
    for char in yo_alphabet:
        names.append(names_by_first_char(char))
    return names

def get_names():
    url = ""

names_by_first_char('a')