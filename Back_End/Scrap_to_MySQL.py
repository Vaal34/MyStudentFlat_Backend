from selenium import webdriver # Importation du module Selenium
from selenium.webdriver.common.by import By # Importation du module By pour les éléments du navigateur
from selenium.webdriver.chrome.options import Options # Importation du module Service pour le service Chrome
import datetime
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, inspect, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from models.Tables import Appartment, Pictures, Base, AdditionalSurfaces, Amenities, BuildingCharacteristics, LeaseRentCharges, PropertyCharacteristics
from Scrap_engine import get_allPages, get_element, save_picture
import json
from sys import argv


# Selenium and Chrome Driver options


# SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/MystudentFlat_test') # Connect to MystudentFlat
inspector = inspect(engine)
if not inspector.has_table('appartment'): # if database exist no create
    Base.metadata.create_all(engine)
sessfactory = sessionmaker(bind=engine) # Create factory session to connect the DB
session = scoped_session(sessfactory) # Creating a "scoped" session that will automatically manage connections based on the context of use

def get_table_appartment(url, session, pageHTML):
    """ Get flat informations """
    Flat = pageHTML.find('div', {'class': 'card'}) # Find all annonce elements on the Flat page
    try:
        # Name
        # Extract the text of the first <h1> element with class "section-title", or set Name to None if no html is found
        Name = Flat.find("h1", {"class": "section-title"}).text if Flat.find("h1", {"class": "section-title"}) else None
        
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
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
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
    except:
        print("l'url n'a pas fonctionné")
        pass

    # Created_at
    created_at = datetime.datetime.now()
    # Add element to the DB with SQLAlchemy
    appart_table = Appartment(name=Name, description=Description, price=Price, ref=Ref, square_meter=Square_meter, address=address, postal_code=postalcode, url=url, agency=agence, phonenumber=None, created_at=created_at) # Create an instance of Appartement 
    session.add(appart_table) # add appart to the current session
    session.commit()
    get_table_picture(session, pageHTML, appart_table, Ref=Ref) # Function thah get all pictures    
    get_table_additionalsurfaces(pageHTML, session, appart_table)
    get_table_amenities(pageHTML, session, appart_table)
    get_table_building_charac(pageHTML, session, appart_table)
    get_table_lease_rent(pageHTML, session, appart_table)
    get_table_PropertyCharac(pageHTML, session, appart_table)

def get_table_picture(session, pageHTML, appart_table, Ref):
    """ Get all pictures"""
    JSONpicture = []
    PictureSection = pageHTML.find("div", {"class", "card"}) # Save class card in variable PictureSection

    imgHTML = PictureSection.find_all("img", class_="photo") # Save all "img" in the variable imgHTML
    if len(imgHTML) != 0: # if picture exist
        srcFirstImage = imgHTML[0]["src"] # store the url picture in srcFirstImage
        response = requests.get(srcFirstImage) # take the status code
        if response.status_code != 500: # if picture have link but dosen't work
            JSONpicture.append(srcFirstImage)
        
        if len(imgHTML) > 1: # if imgHTML have most thant 1 one picture
            src2ndImage = imgHTML[1]["src"] 
            response = requests.get(src2ndImage)
            if response.status_code != 500:
                JSONpicture.append(src2ndImage)
        
        if len(imgHTML) > 2: # if imgHTML have most thant 2 one picture
            src3rdImage = imgHTML[2]["src"] 
            response = requests.get(src3rdImage)
            if response.status_code != 500:
                JSONpicture.append(src3rdImage)
    else: # if picture dosen't exist give a "Picture not found"
        JSONpicture.append("https://www.charlotteathleticclub.com/assets/camaleon_cms/image-not-found-4a963b95bf081c3ea02923dceaeb3f8085e1a654fc54840aac61a57a60903fef.png")
    JSONpicture = json.dumps(JSONpicture) # 
    URL_picture = save_picture(pictures=json.loads(JSONpicture), Ref=Ref) # Function that download all picture in respective file
    URL_picture = json.dumps(URL_picture)
    
    table_picture = Pictures(flat_id=appart_table.id, URL_picture=URL_picture) # Create instance of Picture
    session.add(table_picture) # add Picture instance

def get_table_additionalsurfaces(pageHTML, session, appart_table):
    """ get additional surfaces """
    parking = get_element(pageHTML, className="annexes", element_target="Parking privé") if True else None # Function that get elements needed
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

def api_to_sql_Orpi(index):
        response = requests.get("https://www.orpi.com/recherche/ajax/rent?realEstateTypes%5B%5D=appartement&locations%5B0%5D%5Bvalue%5D=toulouse&locations%5B0%5D%5Blabel%5D=Toulouse+(31000)&maxPrice=800&sort=date-up&layoutType=mixte&recentlySold=false").json()
        
        try:
            data = response["items"][index]
        except IndexError:
            print("Erreur : Index en dehors de la plage valide.")
            return
        
        Name = data["slug"].replace("-", " ").title().split()[:3]
        Name = ' '.join(Name)
        Description = data["longAd"]
        Price = data["price"]
        Ref = data["reference"]
        Square_meter = data["surface"]
        address = data["district"]["name"]
        url = "https://www.orpi.com/annonce-location-" + data["slug"]
        agence = data["agency"]["name"]
        phonenumber = data["agency"]["agencyNumber"]
        created_at = datetime.datetime.now()
        appart_table = Appartment(name=Name, description=Description, price=Price, ref=Ref, square_meter=Square_meter, address=address, postal_code=None, url=url, agency=agence, phonenumber=phonenumber, created_at=created_at) # Create an instance of Appartement 
        session.add(appart_table)
        session.commit()
        # pictures
        pictures = data["images"]
        pictures = json.dumps(pictures)
        URL_picture = save_picture(pictures=json.loads(pictures), Ref=Ref)
        URL_picture = json.dumps(URL_picture)
        table_picture = Pictures(flat_id=appart_table.id, URL_picture=URL_picture)
        session.add(table_picture)
        # additional
        table_additonal_surface = AdditionalSurfaces(flat_id=appart_table.id, Private_parking=None, Cellar=None)
        session.add(table_additonal_surface)
        # amenities
        table_amenties = Amenities(flat_id=appart_table.id, Bathtub=None, Kitchen_sink=None, Washbasin=None, Washing_machine_connection=None, Ventilation_system=None, TV_antenna=None, Shower=None)
        session.add(table_amenties)
        # building
        building_charac_table = BuildingCharacteristics(flat_id=appart_table.id, Year_of_construction=None, Number_of_Floor=None, Digicode=None, Elevator=None, Green_peaces=None, TV_antenna=None, Cleaning_company=None)
        session.add(building_charac_table)
        # lease
        lease_rent_table = LeaseRentCharges(flat_id=appart_table.id, type_of_lease=None, lease_duration=None, rent_charges=None, additional_rent=None, tenant_fess=None, charge_provision=None, check_in_fees=None, security_deposit=None, availability=None)
        session.add(lease_rent_table)
        # property
        propertyCharac_table = PropertyCharacteristics(flat_id=appart_table.id, Floor=None, Total_area=None, Living_area=None, Number_of_rooms=None, Number_of_bedrooms=None, Number_of_bathrooms=None, Hot_water_system=None, Heating_system=None, Double_glazing=None)
        session.add(propertyCharac_table)
        session.commit()
        print("Ajout" + url)

def get_allTables():
    """ Scrap all information of all Flats """
    all_urlFlat = get_allPages() # Call the list of all urls
    count = 0
    for urlpage in all_urlFlat[::-1]: # Loop in list of urls
        response = requests.get(urlpage) # Send a GET request to URL and retrieve the page content
        pagesHTML = BeautifulSoup(response.content, "html.parser") # Parse the HTML content
        get_table_appartment(url=urlpage, session=session, pageHTML=pagesHTML) # Function that get information for on flats
        print(f"élement ajouter a la database {count} {urlpage}")
        print("--------------------------------")
        session.commit() # Commit the changes to the database
        api_to_sql_Orpi(count)
        count += 1
    session.close() # Close the current session

def verify_if_appart_exist():
    """ function that check if an appartment in the databases already exist"""
    list_url_404 = []
    count = 0

    all_appartments = session.query(Appartment).all() # stire the list of all appartment
    
    for appartment in all_appartments:
        url = appartment.url # take the url for each appartment
        response = requests.get(url) # request to the url
        count += 1
        print(url)
        print(count)
        soup = BeautifulSoup(response.content, "html.parser")
        error = soup.select_one('h1.error-message-title').text if soup.select_one('h1.error-message-title') else None # look for the error message
        if error == "Cette annonce n’est plus disponible.": # if we have an error message append to the list of broken url
            list_url_404.append(url)
        elif response.status_code in [404, 410]: # if we have an 404 or 410 append to the list of broken url
            list_url_404.append(url)

    for url404 in list_url_404: # loop for delete in the DB all appartment who dosen't exist
        print(f"Appartment n'existant plus {url404}")
        session.query(Appartment).filter_by(url=url404).delete()
        session.commit()

    session.close()


def add_new_flat():
    """ add new flat in the database if a new is add on the website """
    all_url = get_allPages()
    for url in all_url:
        check_url = session.query(Appartment).filter_by(url=url).first()
        if check_url is None:
            print(url)
            response = requests.get(url) # Send a GET request to URL and retrieve the page content
            pagesHTML = BeautifulSoup(response.content, "html.parser") # Parse the HTML content
            get_table_appartment(url=url, session=session, pageHTML=pagesHTML)
            session.commit()
        else:
            pass
        session.close()

if argv[1] == "check":
    verify_if_appart_exist()
    print("verify check")
elif argv[1] == "add":
    get_allTables()
elif argv[1] == "add_new":
    add_new_flat()
    print("add_new")
elif argv[1] == "orpi":
    api_to_sql_Orpi()
