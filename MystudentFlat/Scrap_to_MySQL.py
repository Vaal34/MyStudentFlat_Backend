from selenium import webdriver # Importation du module Selenium
from selenium.webdriver.common.by import By # Importation du module By pour les éléments du navigateur
from selenium.webdriver.chrome.options import Options # Importation du module Service pour le service Chrome
import datetime
import requests, time
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from models.Tables import Appartment, Pictures, Base, AdditionalSurfaces, Amenities, BuildingCharacteristics, LeaseRentCharges, PropertyCharacteristics
from Scrap_engine import get_allPages, get_element
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
    Price = get_element(pageHTML, className="rent-lease", element_target="Loyer charges comprises") if True else None
    Price = float(Price.split()[0])

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
    chrome_options.add_argument("window-size=1800x1200")
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
    session.commit()
    get_table_picture(session, pageHTML, appart_table) # Function thah get all pictures    
    get_table_additionalsurfaces(pageHTML, session, appart_table)
    get_table_amenities(pageHTML, session, appart_table)
    get_table_building_charac(pageHTML, session, appart_table)
    get_table_lease_rent(pageHTML, session, appart_table)
    get_table_PropertyCharac(pageHTML, session, appart_table)

def get_table_picture(session, pageHTML, appart_table):
    """ Get all pictures"""
    if pageHTML.find("div", {"class", "photos"}):
        PictureSection = pageHTML.find("div", {"class", "photos"})
    
        imgHTML = PictureSection.find_all("img", class_="photo")
        srcFirstImage = imgHTML[0]["src"]
        src2ndImage = imgHTML[1]["src"] if len(imgHTML) > 1 else None
        src3rdImage = imgHTML[2]["src"] if len(imgHTML) > 2 else None
        JSONpicture = [srcFirstImage, src2ndImage, src3rdImage]
        JSONpicture = json.dumps(JSONpicture)
    else:
        JSONpicture = None
    table_picture = Pictures(flat_id=appart_table.id, URL_picture=JSONpicture)
    session.add(table_picture)

def get_table_additionalsurfaces(pageHTML, session, appart_table):
    """ get additional surfaces """
    parking = get_element(pageHTML, className="annexes", element_target="Parking privé") if True else None
    cellar = get_element(pageHTML, className="annexes", element_target="Cave(s)") if True else None
    table_additonal_surface = AdditionalSurfaces(flat_id=appart_table.id, Private_parking=parking, Cellar=cellar)
    session.add(table_additonal_surface)

def get_table_amenities(pageHTML, session, appart_table):
    """ get all amenities"""
    Bathtub = get_element(pageHTML, className="equipments", element_target="Baignoire") if True else None
    Kitchen_sink = get_element(pageHTML, className="equipments", element_target="Evier de cuisine") if True else None
    Washbasin = get_element(pageHTML, className="equipments", element_target="Lavabo") if True else None
    Washing_machine_connection = get_element(pageHTML, className="equipments", element_target="Branchement(s) machine à laver") if True else None
    Ventilation_system = get_element(pageHTML, className="equipments", element_target="Système de ventilation") if True else None
    TV_antenna = get_element(pageHTML, className="equipments", element_target="Antenne TV") if True else None
    Shower = get_element(pageHTML, className="equipments", element_target="Douche") if True else None

    table_amenties = Amenities(flat_id=appart_table.id, Bathtub=Bathtub, Kitchen_sink=Kitchen_sink, Washbasin=Washbasin, Washing_machine_connection=Washing_machine_connection, Ventilation_system=Ventilation_system, TV_antenna=TV_antenna, Shower=Shower)
    session.add(table_amenties)

def get_table_building_charac(pageHTML, session, appart_table):
    """ get all Building Characteristics"""
    Year_of_construction = get_element(pageHTML, className="building", element_target="Année de construction") if True else None
    Number_of_Floor = get_element(pageHTML, className="building", element_target="Nombre d'étages") if True else None
    Digicode = get_element(pageHTML, className="building", element_target="Digicode") if True else None
    Elevator = get_element(pageHTML, className="building", element_target="Ascenseur") if True else None
    Green_peaces = get_element(pageHTML, className="building", element_target="Espaces verts") if True else None
    TV_Antenna = get_element(pageHTML, className="building", element_target="Antenne TV") if True else None
    Cleaning_company = get_element(pageHTML, className="building", element_target="Société de nettoyage") if True else None
    building_charac_table = BuildingCharacteristics(flat_id=appart_table.id, Year_of_construction=Year_of_construction, Number_of_Floor=Number_of_Floor, Digicode=Digicode, Elevator=Elevator, Green_peaces=Green_peaces, TV_antenna=TV_Antenna, Cleaning_company=Cleaning_company)
    session.add(building_charac_table)

def get_table_lease_rent(pageHTML, session, appart_table):
    """ get all lease & rent information """
    type_of_lease = get_element(pageHTML, className="rent-lease", element_target="Type de bail") if True else None
    lease_duration = get_element(pageHTML, className="rent-lease", element_target="Durée Bail") if True else None
    rent_charges = get_element(pageHTML, className="rent-lease", element_target="Loyer charges comprises") if True else None
    additional_rent = get_element(pageHTML, className="rent-lease", element_target="Dont complément de loyer") if True else None
    tenant_fess = get_element(pageHTML, className="rent-lease", element_target="Honoraires charge locataire") if True else None
    charge_provision = get_element(pageHTML, className="rent-lease", element_target="Dont provision sur charges (Regularisation Annuelle)") if True else None
    check_in_fees = get_element(pageHTML, className="rent-lease", element_target="Dont état des lieux") if True else None
    security_deposit = get_element(pageHTML, className="rent-lease", element_target="Dépôt de garantie") if True else None
    availability = get_element(pageHTML, className="rent-lease", element_target="Disponibilité") if True else None
    lease_rent_table = LeaseRentCharges(flat_id=appart_table.id, type_of_lease=type_of_lease, lease_duration=lease_duration, rent_charges=rent_charges, additional_rent=additional_rent, tenant_fess=tenant_fess, charge_provision=charge_provision, check_in_fees=check_in_fees, security_deposit=security_deposit, availability=availability)
    session.add(lease_rent_table)

def get_table_PropertyCharac(pageHTML, session, appart_table):
    """ get all informations of property characteristics """
    Floor = get_element(pageHTML, className="property", element_target="Etage") if True else None
    Total_area = get_element(pageHTML, className="property", element_target="Surface totale") if True else None
    if Total_area is not None:
        Total_area = float(Total_area.split()[0]) if "." in Total_area else Total_area.split()[0]
    Living_area = get_element(pageHTML, className="property", element_target="Surface habitable") if True else None
    if Living_area is not None:
        Living_area = float(Living_area.split()[0]) if "." in Living_area else Living_area.split()[0]
    Number_of_rooms = get_element(pageHTML, className="property", element_target="Nombre de pièces") if True else None
    Number_of_bedrooms = get_element(pageHTML, className="property", element_target="Nombre de chambres") if True else None
    Number_of_bathrooms = get_element(pageHTML, className="property", element_target="Nombre de salles de bain") if True else None
    Hot_water_system = get_element(pageHTML, className="property", element_target="Eau chaude") if True else None
    Heating_system = get_element(pageHTML, className="property", element_target="Chauffage") if True else None
    Double_glazing = get_element(pageHTML, className="property", element_target="Double vitrage") if True else None
    propertyCharac_table = PropertyCharacteristics(flat_id=appart_table.id, Floor=Floor, Total_area=Total_area, Living_area=Living_area, Number_of_rooms=Number_of_rooms, Number_of_bedrooms=Number_of_bedrooms, Number_of_bathrooms=Number_of_bathrooms, Hot_water_system=Hot_water_system, Heating_system=Heating_system, Double_glazing=Double_glazing)
    session.add(propertyCharac_table)

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
