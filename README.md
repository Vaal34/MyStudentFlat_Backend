![MyStudentFlat](https://github.com/Amandine4731/holbertonschool-MyStudentFlat/blob/amandine/Flutter/my_student_flat_advanced/assets/elements/logoMyStudentFlatOrange.png?raw=true)

*****
This application project is part of a end-of-year project at **Holberton Actual Digital School** in Toulouse.

### **Are you a student? Looking for an apartment? This application might interest you!**
My Student Flat is an application mainly intended for the student population of Toulouse. It brings together all the affordable apartments (< €800.00) in the city of Toulouse (31). The goal? To allow all these students to not spend all their time in an intense search for housing.

### **A project, a team**
This application could not exist without the collaboration of two individuals with complementary skills. Amandine Assenat (20 years old) is developing the front-end part, an obvious choice given her background as a graphic designer. Valentin Melia (23 years old) is responsible for creating his own API, which gathers all the apartments in Toulouse. This synergy is the result of this project.

*****

### **Strategically chosen technologies used:**
**Front-end**
- **Flutter (Dart):** The Dart language has advanced features. Flutter has a simple syntax, allowing for the development of an application in two weeks. Flutter has become popular and offers a wide range of resources. It is also suitable for Android and iOS platforms.
**Back-end**
- **Python:** Python is a simple and readable language. It is known for its clear and concise syntax. Python has a large number of libraries for creating APIs, such as Flask, Django, FastAPI, and CherryPy. These libraries facilitate API development and offer many predefined features.
- **MySQL:** MySQL is one of the most popular databases in the world, with a large community of developers and contributors providing abundant documentation and active support.
- **SQLAlchemy:** Enables the connection between web scraping and the database.
- **Flask:** Flask is a library that allows easy customization of an application according to its needs by creating routes.

*****

### **File tree**

- **AUTHORS:**
- **README.md:**

#### **Front-end**
    
| **Folders** | **Files** | Description |
|----------|-----------------------------------------------|----------------------|
| assets | | Contains all the images and illustrations |
| | analysis_options.yaml | Determines how strict Flutter should be when analyzing your code. |
| | pubspec.yaml | Groups all dependencies that the project requires, such as particular packages, fonts, or image files,... |
| lib | | Contains all the elements present on the screen |
| | -> main.dart | Main file that launches the application |  
| -> pages | Contains the 6 pages of the application |  |
| | -> page_signup.dart | Page to create an account |
| | -> page_login.dart | Page to log in with an account |
| | -> page_home.dart | Home page that gathers all the apartment listings |
| | -> page_description.dart | Page with all the information about each apartment |
| | -> page_account_changing.dart | Page to delete an account |
| | -> page_filters.dart | Page to refine the search, advanced functionalities of the application |
| -> components | | Contains all the necessary elements for layout |
| | -> component_navigation_home_appbar.dart | Top navigation bar for the home page |
| | -> component_navigation_appbar.dart | Top navigation bar |
| | -> component_navigation_bottomappbar.dart | Bottom navigation bar |
| | -> component_card_flat.dart | Card present on the home page. One card = one apartment listing |
| | -> component_pictures_carousel.dart | Scroll through all the images |
| | -> component_pictures_full_screen.dart | Enlarge the images in the description page |
| | -> component_choices_localization.dart | Filter listings by location |
| | -> component_choices_number_of_pieces.dart | Filter listings by the number of rooms |
| | -> component_slider_bar_area.dart | Filter listings by the area of the property |
| | -> component_slider_bar_price.dart | Filter listings by the rent price |
| | -> component_choices_other_criteria.dart | Filter listings by advanced criteria |
| | -> component_local_notifications.dart | Display notifications |
| -> effets | | Contains effects |
| | -> effect_animation_dalayed.dart | Create an elevation effect on buildings on the signup and login pages |
| -> API | | Database |
| | -> album.dart | Collects all the keys and values of the API |
| | -> request_pictures.dart | Retrieve all the images for each apartment |
| | -> request_values.dart | Retrieve all the information for each apartment |

#### **Back-end**
    
| **Folders** | **Files** | Description |
|----------|-----------------------------------------------|----------------------|
|  |  |  |



*****

### **What does MyStudentFlat look like?**
*(add photos)*


### The repository:
```bash
$ git clone https://github.com/Amandine4731/holbertonschool-MyStudentFlat.git
```

*By Valentin Melia and Amandine Assenat*
