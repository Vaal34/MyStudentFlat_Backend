-- Create the table appartment(Parent)
CREATE TABLE appartment (Flat_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), price INT, ref INT, description TEXT, Square_meter INT, Adress VARCHAR(255), Postal_code INT, url VARCHAR(255));
-- Create the table lease, rent and charges
CREATE TABLE lease_rent_charges (Rent_id INT PRIMARY KEY, FOREIGN KEY (Rent_id) REFERENCES appartment(Flat_id) ON DELETE CASCADE, Type_of_lease VARCHAR(256), Lease_duration VARCHAR(255), Rent_charges VARCHAR(255), Additional_rent VARCHAR(255), Tenant_fess VARCHAR(255), Charge_provision VARCHAR(255), Check_in_fees VARCHAR(255), Security_deposit VARCHAR(255), Availability VARCHAR(255));
-- Create the table Building characteristics
CREATE TABLE building_characteristics (Charac_Build_Id INT PRIMARY KEY, FOREIGN KEY (Charac_Build_Id) REFERENCES appartment(Flat_id) ON DELETE CASCADE, Year_of_construction INT, Number_of_Floor INT, Digicode VARCHAR(5), Videophone VARCHAR(5), Elevator VARCHAR(5), Green_peaces VARCHAR(5));
-- Create the table Annexes and additional surfaces
CREATE TABLE additional_surfaces (Additional_surface_id INT PRIMARY KEY, FOREIGN KEY (Additional_surface_id) REFERENCES appartment(Flat_id) ON DELETE CASCADE, Cellar INT, Private_parking INT);
-- Create the table Amenities
CREATE TABLE amenities (amenities_id INT PRIMARY KEY, FOREIGN KEY (amenities_id) REFERENCES appartment(Flat_id) ON DELETE CASCADE, Bathtub VARCHAR(5), Kitchen_sink VARCHAR(10), Washbasin VARCHAR(5), Washing_machine_connection VARCHAR(5), Ventilation_system VARCHAR(5), TV_antenna VARCHAR(5));
-- Create the table Property Characteristics
CREATE TABLE property_characteristics (Chara_Proper_Id INT PRIMARY KEY, FOREIGN KEY (Chara_Proper_Id) REFERENCES appartment(Flat_id) ON DELETE CASCADE, Floor INT, Total_area INT, Living_area INT, Number_of_rooms INT, Number_of_bedrooms INT, Number_of_bathrooms INT, Hot_water_system VARCHAR(45), Heating_system VARCHAR(45), Double_glazing VARCHAR(45));
-- Create the table picture
CREATE TABLE pictures (Picture_id INT PRIMARY KEY, FOREIGN KEY (Picture_id) REFERENCES appartment(Flat_id) ON DELETE CASCADE, URL_picture VARCHAR(255));