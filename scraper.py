from bs4 import BeautifulSoup as bs4
import requests
import re

#TODO:
#Safely access the name infos in the get_name_info method



yo_alphabet = ['a','b','d','e','ẹ','f','g','gb','h','i','j','k','l','m','n','o','ọ','p','r','s','ṣ','t','u','w','y']

#Returns the all names with the first character passed
def names_by_first_char(first_char):
    url = "https://www.yorubaname.com/alphabet/" + first_char
    page = requests.get(url=url).text
    if page.status_codes != 200:
        return {"Error:","Something Went Wrong During the Request"}
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
    if page.status_codes != 200:
        return {"Error:","Something Went Wrong During the Request"}
    soup = bs4(page,"html.parser")
    info_dict = {}

    #Element var used to store the element before it is checked whether it is None to avoid errors
    element = soup.find("h2",id="name-entry")
    info_dict["Name"] = element.text #Returns version of name(with diacritics) listed, not (possibly) non-diacrticized version
    
    element = soup.find("h4",string=re.compile(r'Meaning of .*'))
    if element is not None: info_dict["Meaning"] = element.find_next('p').text
    
    element =  soup.find("h4",string=re.compile(r'Extended Meaning'))
    if element is not None: info_dict["Extended Meaning"] = element.find_next('p').text
    
    element = soup.find("h4",string=re.compile(r'Morphology'))
    if element is not None: info_dict["Morphology"] = element.find_next('p').text
    
    if soup.find("h4",string=re.compile(r'Gloss')) is not None:
        #Get Different Parts of Gloss - I'm not sure if this method always works but SHOULD BE TESTED
        num_parts = len(info_dict['Morphology'].split('-'))# Note I can't just search for each seperate part - wouldn't work for cases like https://www.yorubaname.com/entries/Fa%CC%81di%CC%80mu%CC%81la%CC%80 where Morphology and Gloss parts don't exactly match
        start_point = soup.find("h4",string=re.compile(r'Gloss'))
        parts = []
        for i in range(0,num_parts):
            parts.append(start_point.find_next("strong").text + start_point.find_next("span").text)
            start_point = start_point.find_next("span")
        
        info_dict["Gloss"] = parts

    #get Geolocation by finding Geolocation header, then paragraph, then using a regex search to capture the text from "Common in: X"
    if soup.find("h4",string=re.compile(r'Geolocation')):
        info_dict["Geolocation"] = re.search(r'Common in:\s*(\w+)',soup.find("h4",string=re.compile(r'Geolocation')).find_next('p').text).group(1)
    pronun_url = f"https://tts.yorubaname.com/api/v1/names/{info_dict["Name"]}"
    if requests.get(pronun_url).status_code == 200:
        info_dict["Pronunciation_URL"] = pronun_url
    if soup.find("h4", string=re.compile(r'Variants')):
        iterator_element = soup.find("h4", string=re.compile(r'Variants')).find_next("p", class_="name")
        variants = []
        while iterator_element:
            variants.append(iterator_element.text.strip())
            iterator_element = iterator_element.find_next("p", class_="name")
        info_dict["Variants"] = variants

    return info_dict



#names_by_first_char('a')
print(get_name_info(r'Ebigbola'))
print(r"\n\n\n\n")
print(get_name_info(r'Oyin'))