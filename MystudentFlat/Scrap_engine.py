import requests, time
from bs4 import BeautifulSoup

def get_number_pages():
    """ get the number of existing pages """
    url = "https://fr.foncia.com/location/toulouse-31?prix=--800&advanced=" # URL page 1
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find("ol") # Get <ol> balise in HTML of the pages
    page_number = links.text # Get just the text in all <ol><li>
    list_page_number = [int(num) for num in page_number.split()] # Append in a list just the number without whitespace
    return max(list_page_number) # Get the max number of the list

def get_allPages():
    """ Get all flat url Pages """
    all_urls = [] # Contains all urls of flat pages
    number_of_pages = get_number_pages() # get number of pages with all flats
    for page_number in range(1, number_of_pages+1): # loop who iterates in the pages with all flat with the url_template 
        url_template = f"https://fr.foncia.com/location/toulouse-31/appartement?prix=--800&page={page_number}&advanced="
        response = requests.get(url_template) # retrieve the html
        pageHTML = BeautifulSoup(response.content, "html.parser") # parse the html
        allFlat = pageHTML.find_all('app-annonce-card') # Find all annonce elements on the page
        for baliseHTML in allFlat: # loop who iterate in the html page and select all url of all Flats on the page
            url = baliseHTML.find("a", {"class": "gallery-container"}).get("href") # retrives all urls
            all_urls.append("https://fr.foncia.com" + url) # append and create url in the list
    return all_urls # return all urls in a list

def get_element(pageHTML, className, element_target):
    Part_HTML = pageHTML.find("div", {"class": className}) if pageHTML.find("div", {"class": className}) else None
    balise_before_info = Part_HTML.find('span', string=element_target).previous_element if Part_HTML.find('span', string=element_target) else None
    if balise_before_info:
        return balise_before_info.next_sibling.text.strip()
