from bs4 import BeautifulSoup as bs4
import requests
import re

#TODO:
#Safely access the name infos in the get_name_info method
#Add Request Safeties
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

def get_name_info(name):
    url = "https://www.yorubaname.com/entries/" + name
    page = requests.get(url=url).text
    soup = bs4(page,"html.parser")

    info_dict = {}
    #soup.select(soup.find("div",class_="col-sm-7"))
    info_dict["Name"] = soup.find("h2",id="name-entry").text #Returns version of name(with diacritics) listed, not (possibly) non-diacrticized version
    info_dict["Meaning"] = soup.find("h4",string=re.compile(r'Meaning of .*')).find_next('p').text
    info_dict["Extended Meaning"] = soup.find("h4",string=re.compile(r'Extended Meaning')).find_next('p').text
    info_dict["Morphology"] = soup.find("h4",string=re.compile(r'Morphology')).find_next('p').text
    
    #Get Different Parts of Gloss - I'm not sure if this method always works but SHOULD BE TESTED
    num_parts = len(info_dict['Morphology'].split('-'))# Note I can't just search for each seperate part - wouldn't work for cases like https://www.yorubaname.com/entries/Fa%CC%81di%CC%80mu%CC%81la%CC%80 where Morphology and Gloss parts don't exactly match
    start_point = soup.find("h4",string=re.compile(r'Gloss'))
    parts = []
    for i in range(0,num_parts):
        parts.append(start_point.find_next("strong").text + start_point.find_next("span").text)
        start_point = start_point.find_next("span")
    
    info_dict["Gloss"] = parts

    #get Geolocation by finding Geolocation header, then paragraph, then using a regex search to capture the text from "Common in: X"
    info_dict["Geolocation"] = re.search(r'Common in:\s*(\w+)',soup.find("h4",string=re.compile(r'Geolocation')).find_next('p').text).group(1)




    return info_dict



#names_by_first_char('a')
print(get_name_info(r'Ebigbola'))