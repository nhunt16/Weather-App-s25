# Temperature and Humidity 2019-mini-s25

 Authors: Nicolas Hunt and Elizabeth Slade

### Instructions to run the app on your local machine
See requirements.txt for dependencies

  1. activate your venv
  2. run: pip install -r requirements.txt
  
### [Website where the Software Mini Project Application is hosted](http://emslade.pythonanywhere.com/)

### Introduction
For the ENG EC 463 mini project, team s25 consisting of Nicolas and Elizabeth, developed a web application to satisfy project specifications. Our site allows users to add, manage, and view their temperature and humidity sensor data over 24 hours.

### Team s25
Nicolas Hunt - Database design, database implementation, sensor data generation, web server implementation, report writing

Elizabeth Slade - Database design, SSO, cloud hosting, data visualizations, CSS, report writing

### Primary Tools
  1. flask - web application framework for Python
  2. sqlalchemy - object-relational mapper (ORM) for Python
  3. sqlite - relational database management system, embedded database software
  4. python anywhere - cloud hosting service
  5. google authentication - single sign on (SSO)
  
### Technical Approach
  
We used flask as our web application framework because of its ease-of-use and the team’s general familiarity with python. Flask allows us to pass data to html files and render them, which is particularly useful for displaying data including user locations and visualizations. We used another python library, sqlalchemy to generate, edit, and update our database via python objects. sqlalchemy is powerful and integrates well with flask. For our database we chose sqlite because it is perfect to use on smaller, rapid development projects like this one. Since sqlite is a local storage system, we can easily view and manage our data with DB Browser for SQLite. The transition to enterprise database management systems for scalability is very simple and would require little to no changes to the code. For cloud hosting we chose a free service called python anywhere. The reason for this was because the hosting service provides access to a bash console on the server you are deploying tol, so you can effectively install and update all necessary libraries.

### Project Details and Specifications
- Single Sign On: We used Google single sign on for our application. In particular we used autho library and flask-login library.
- The application can be iOS, Android or WEB application: We used a WEB application. In particular we used Flask as our framework.
- You can use any cloud service provider: We used Python Anywhere as our cloud service provider to host the application online. 
- You can use any database including database services: We used SQLite for our database
- Weather data: We randomly generate weather data based on location.
- Current Location: We have a current location functionality where a user can input their current location and then the temperature and humidity data is displayed on the homepage.
- Multiple users with multiple locations: We created a database schema where we can store multple users and each user can have multiple locations. See below for more details on this.

### Technical Notes
Our database leverages 5 tables. The first is a User table which keeps track of all users by storing their email and assigned unique user id number (uid). The second is a Locations table which maps every sensor location to a unique location id number (lid). The third is a UserLocations table which maps uid to lid, meaning that when a user adds a new location the corresponding lid will be linked to their uid. The fourth and fifth tables store hourly temperature and humidity data for the given day. They each map 24 data points to an lid and store just the most recent time stamp (since the rest of the time data can be easily calculated). This database schema eliminates the need to store data, including temperature/humidity, into strings or otherwise difficult to parse and manage entries and everything is clearly linked using unique identifiers. 

For testing we did extensive unit tests to ensure that our web application handles inputs correctly. Our testing exposed several bugs that we then fixed, including duplicate user data in database, mishandling of sensor names with different capitalizations, and so on. 

### Task Management
- We split the project into smaller tasks and distributed the work between us. We typically wrote and distributed tasks on paper and have virtualized them onto [Trello](https://trello.com/b/rul6MZm5/s25-weather-app).



