import requests, time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.Tables import Appartment, AdditionalSurfaces, Amenities, LeaseRentCharges, BuildingCharacteristics, PropertyCharacteristics, Pictures

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/MystudentFlat') # Connect to MystudentFlat

sessfactory = sessionmaker(bind=engine) # Create factory session to connect the DB
session = scoped_session(sessfactory) # Creating a "scoped" session that will automatically manage connections based on the context of use

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

def get_flat(url, session):
    """ Get flat informations """
    response = requests.get(url) # Send a GET request to URL and retrieve the page content
    pagesHTML = BeautifulSoup(response.content, "html.parser") # Parse the HTML content
    for noNeed in pagesHTML.find_all(['script', 'style']): # Remove all balise <script> and <style>
        noNeed.decompose()
    Flat = pagesHTML.find('div', {'class': 'card'}) # Find all annonce elements on the Flat page
    if Flat.find('h1', {'class': 'section-title'}): # Only if the Name exist
        Name = Flat.find('h1', {'class': 'section-title'}).text
    else:
        Name = None
    if Flat.find('p', {'class': 'section-description'}): # Only if the Description exist
        Description = Flat.find('p', {'class': 'section-description'}).text
    else:
        Description = None
    if Flat.find('p', {'class': 'value'}): # Only if the Price exist
        price_response = Flat.find('p', {'class': 'value'}).text
        price_str = price_response.replace(',', '.').replace('€', '') # replace comma by dot and delete € for convert in float
        Price = float(price_str)
    else:
        Price = None
    if Flat.find('p', {'class': 'section-reference'}): # Only if the référence exist
        ref_response = Flat.find('p', {'class': 'section-reference'}).text
        ref_str = ref_response.split(' ')[2] # split Ref. 283948 for take just the integer
        Ref = int(ref_str)
    else:
        Ref = None
    appart = Appartment(name=Name, description=Description, price=Price, ref=Ref) # Create an instance of Appartement 
    session.add(appart) # add appart to the current session  

def get_allflat():
    """ Scrap all information of all Flats """
    all_urlFlat = get_allPages() # Call the list of all urls
    count = 1
    for urlpage in all_urlFlat: # Loop in list of urls
        get_flat(url=urlpage, session=session) # Function that get information for on flats
        print(f"élement ajouter a la database {count}")
        count += 1
        session.commit() # Commit the changes to the database
    session.close() # Close the current session

while True:
    get_allflat()
    tile = time.sleep(3600)
