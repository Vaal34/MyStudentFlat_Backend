import requests, time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.Tables import Appartment, AdditionalSurfaces, Amenities, LeaseRentCharges, BuildingCharacteristics, PropertyCharacteristics, Pictures
from Scrap_engine import get_allPages

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/MystudentFlat') # Connect to MystudentFlat

sessfactory = sessionmaker(bind=engine) # Create factory session to connect the DB
session = scoped_session(sessfactory) # Creating a "scoped" session that will automatically manage connections based on the context of use

def get_flat_informations(url, session):
    """ Get flat informations """
    response = requests.get(url) # Send a GET request to URL and retrieve the page content
    pagesHTML = BeautifulSoup(response.content, "html.parser") # Parse the HTML content
    for noNeed in pagesHTML.find_all(['script', 'style']): # Remove all balise <script> and <style>
        noNeed.decompose()
    Flat = pagesHTML.find('div', {'class': 'card'}) # Find all annonce elements on the Flat page
    
    # Name
    if Flat.find('h1', {'class': 'section-title'}): # Only if the Name exist
        Name = Flat.find('h1', {'class': 'section-title'}).text
    else:
        Name = None
    
    # Description
    if Flat.find('p', {'class': 'section-description'}): # Only if the Description exist
        Description = Flat.find('p', {'class': 'section-description'}).text
    else:
        Description = None
    
    # Price
    if Flat.find('p', {'class': 'value'}): # Only if the Price exist
        price_response = Flat.find('p', {'class': 'value'}).text
        price_str = price_response.replace(',', '.').replace('€', '') # replace comma by dot and delete € for convert in float
        Price = float(price_str)
    else:
        Price = None
    
    # Ref
    if Flat.find('p', {'class': 'section-reference'}): # Only if the référence exist
        Ref = Flat.find('p', {'class': 'section-reference'}).text
    else:
        Ref = None
    
    # Square meter
    if Flat.find('div', {'class': 'surface'}):
        response_Smeter = Flat.find('div', {'class': 'surface'}).text
        Square_meter = float(response_Smeter.replace(',', '.').split(' ')[0])

    else:
        Square_meter = None

    # Adress
    Location = Flat.find('p', {'class': 'location'})
    if Location.find('span', {'class': 'p-mb-2'}):
        address = Location.find('span', {'class': 'p-mb-2'}).text
    else:
        address = None
    
    # Postal Code
    if Location.find('span', {'class': 'zipcode'}):
        postalcode = Location.find('span', {'class': 'zipcode'}).text
    else:
        postalcode = None

    appart = Appartment(name=Name, description=Description, price=Price, ref=Ref, square_meter=Square_meter, adress=address, postal_code=postalcode, url=url) # Create an instance of Appartement 
    session.add(appart) # add appart to the current session  

def get_allflat():
    """ Scrap all information of all Flats """
    all_urlFlat = get_allPages() # Call the list of all urls
    count = 1
    for urlpage in all_urlFlat: # Loop in list of urls
        get_flat_informations(url=urlpage, session=session) # Function that get information for on flats
        print(f"élement ajouter a la database {count}")
        count += 1
        session.commit() # Commit the changes to the database
    session.close() # Close the current session

get_allflat()
