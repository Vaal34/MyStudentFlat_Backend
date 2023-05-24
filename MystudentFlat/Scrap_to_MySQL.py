from selenium import webdriver # Importation du module Selenium
from selenium.webdriver.common.by import By # Importation du module By pour les éléments du navigateur
from selenium.webdriver.chrome.options import Options # Importation du module Service pour le service Chrome
import datetime
import requests, time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from models.Tables import Appartment, Pictures, Base
#from models.Tables import Appartment, AdditionalSurfaces, Amenities, LeaseRentCharges, BuildingCharacteristics, PropertyCharacteristics, Pictures, Base
from Scrap_engine import get_allPages
from selenium.webdriver.common.action_chains import ActionChains
import json

# Selenium and Chrome Driver options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/MystudentFlat_test') # Connect to MystudentFlat
inspector = inspect(engine)
if not inspector.has_table('appartment'): # if database exist no create
    Base.metadata.create_all(engine)
sessfactory = sessionmaker(bind=engine) # Create factory session to connect the DB
session = scoped_session(sessfactory) # Creating a "scoped" session that will automatically manage connections based on the context of use

def get_table_informations(url, session, pageHTML):
    """ Get flat informations """
    Flat = pageHTML.find('div', {'class': 'card'}) # Find all annonce elements on the Flat page
    
    # Name
    # Extract the text of the first <h1> element with class "section-title", or set Name to None if no html is found
    Name = Flat.select_one('h1.section-title').text if Flat.select_one('h1.section-title') else None
    
    # Description
    # Extract the text of the first <p> element with class "section-description", or set Description to None if no html is found
    Description = Flat.select_one('p.section-description').text if Flat.select_one('p.section-description') else None

    # Price
    if Flat.find('p', {'class': 'value'}): # Only if the Price exist
        price_response = Flat.find('p', {'class': 'value'}).text
        price_str = price_response.replace(',', '.').replace('€', '') # replace comma by dot and delete € for convert in float
        Price = float(price_str)
    else:
        Price = None
    
    # Ref
    # Extract the text of the first <p> element with class "section-reference", or set Ref to None if no html is found
    Ref = Flat.select_one('p.section-reference').text if Flat.select_one('p.section-reference') else None

    # Square meter
    # Extract the numeric value (1234 without m²) from the text content of the element, or set Square_meter to None if no html is found
    surface = Flat.select_one('div.surface') # Find the first <div> element with class "surface"
    Square_meter = float(surface.text.replace(',', '.').split(' ')[0]) if surface else None 

    # Adress
    Location = Flat.find('p', {'class': 'location'})
    # Extract the text of the first <span> element with class "p-mb-2", or set address to None if no html is found
    address = Location.select_one('span.p-mb-2').text if Location.select_one('span.p-mb-2') else None
    # Extract the text of the first <span> element with class "zipcode", or set postal to None if no html is found
    postalcode = Location.select_one('span.zipcode').text if Location.select_one('span.zipcode') else None

    # Agency
    # Extract the text of the first <p> <a> element with class "agency-card-agency-name", or set agence to None if no html is found
    agence = pageHTML.select_one('p.agency-card-agency-name a').text if pageHTML.select_one('p.agency-card-agency-name a') else None

    # Phone Number
    chrome_options.add_argument("window-size=1600x1200")
    driver = webdriver.Chrome(options=chrome_options) # Instance of Chrome driver
    driver.get(url) # Open webpage
    try:
        driver.find_element(By.CLASS_NAME, "agency-card-contact").click()
        driver.find_element(By.CLASS_NAME, "agency-card-contact-buttons").find_element(By.CLASS_NAME, "show-button").click()
        if driver.find_element(By.CLASS_NAME, "show-button").text:
            PhoneNumber = driver.find_element(By.CLASS_NAME, "show-button").text
        else:
            PhoneNumber = None
    except:
            PhoneNumber = None
    driver.quit()

    # Created_at
    created_at = datetime.datetime.now()
    # Add element to the DB with SQLAlchemy
    appart_table = Appartment(name=Name, description=Description, price=Price, ref=Ref, square_meter=Square_meter, address=address, postal_code=postalcode, url=url, agency=agence, phonenumber=PhoneNumber, created_at=created_at) # Create an instance of Appartement 
    session.add(appart_table) # add appart to the current session
    get_table_picture(url, session, pageHTML, appart_table) # Function thah get all pictures    


def get_table_picture(url, session, pageHTML, appart_table):
    """ Get all pictures"""

    PictureSection = pageHTML.find("div", {"class", "photos"})
    
    imgHTML = PictureSection.find_all("img", class_="photo")
    srcFirstImage = imgHTML[0]["src"]
    src2ndImage = imgHTML[1]["src"] if len(imgHTML) > 1 else None
    src3rdImage = imgHTML[2]["src"] if len(imgHTML) > 2 else None

    JSONpicture = [srcFirstImage, src2ndImage, src3rdImage]
    table_picture = Pictures(flat_id=appart_table.id, URL_picture=json.dumps(JSONpicture))
    # flat_id est NuLLLL
    session.add(table_picture)

def get_allTables():
    """ Scrap all information of all Flats """
    all_urlFlat = get_allPages() # Call the list of all urls
    count = 1
    for urlpage in all_urlFlat: # Loop in list of urls
        response = requests.get(urlpage) # Send a GET request to URL and retrieve the page content
        pagesHTML = BeautifulSoup(response.content, "html.parser") # Parse the HTML content
        for noNeed in pagesHTML.find_all(['script', 'style']): # Remove all balise <script> and <style>
            noNeed.decompose()
        get_table_informations(url=urlpage, session=session, pageHTML=pagesHTML) # Function that get information for on flats
        print(f"élement ajouter a la database {count} {urlpage}")
        count += 1
        session.commit() # Commit the changes to the database
    session.close() # Close the current session

get_allTables()
