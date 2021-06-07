# Charging stations, Group 38, KEA

## Creators
Filip Gavalier, David Usvat, Ibrahim Muhamed, Chen Mae N. Pantua, Erkan Ahmed, Ildikó Péter

## Languages used 
Python, MySQL

## Usage
The main usage of this python script is to locate all possible charging stations in the area of Denmark. The location of each charging station comes in a csv file.
Furthermore, it can log an existing user in using MySQL database, as well as register a new user and store the information in the database. Using the user's information, the program then has an option to show user's personal consumption and status update on the charging of their vehicle.

## Requirements
````
import folium
from folium.plugins import FloatImage
import pandas as pd
import mysql.connector as sql
import time
import webbrowser
from time import sleep
````
In order for this code to work, one must make sure that they have installed the correct libraries. The code above shows which ones you will need, as well as a way of how to import them and use them in your code.
````
pip install name_of_the_library
````
Run this command in your terminal to install the libraries. Obviously don't forget to substitute _name_of_the_library_ with an actual library name :)

What's more, you will need a MySQL database, for which we have provided a code for. All you need to do is run it in MySQL workbench. There is one problem though, after you are done cith creating the database, you will need to manually import the data about charging stations. We have provided you with a csv file, which you need to save. Afterwards, right click the newly-created schema(exam2) and select Table Data Import Wizard. Import the data into an existing table called charging_stations. 

## Class Log_in()
The code starts with an introduction, explaining what the code does, then a first input is created to find out whether the user is an existing or a new one.
Subsequently, a class Log_in is created to connect python with MySQL database and verify/register the user in the database. 
````
__HOST= "localhost"
__USERNAME= "root"
__PASSWORD= "FilipFG7"
__DATABASE= "exam2"
````
**You will need to change these information and input your own.** You can see the information by right clicking your MySQL connection and selecting the _edit connection_ option.

The first function of the class states the connect script for MySQL connector and stores it in _self.con_.

The function _veryfying()_ does two things. If you are an existing user, it will check the database for your information. It contains two user's input for the First and Last name. It defines _mycursor_, through which we are able to run MySQL commands in the database with python using _mycursor.execute(_). 
If you are a new user, the function then asks the user for their first and last name and the car model. Subsequently it stores all the data inside the database, which will assign the user and the car with its own ID. We use _self.con.commit()_ to save the changes.

The function _check_consumption()_ is also devided into two parts using if and else statement. If you are an existing user, it will use MySQL _Select_ statement to display the _personal consumption_ of the user. For the new users, we had to create a _try except_ statement. This is due to the fact, that in the begining the new user would not have any consumption yet. However, in the following function of the class _status_update()_, the user can add minutes into his consumption, therefore it would not show the updated consumption if we would not do it this way.

As we have already mentioned, in the _status_update()_ function of the class, the user is able to select how many minutes should the car be charging for and then it updates the database table by adding the selected minutes with the personal consumption up to that point. Normally, this function would give you a real update on the charging, but since we don't have an access to the actual live data of the charging stations, nor do we have an electric car, we found this task to be impossible. Due to this we created kind of like a simulation of how it might work. 

## Function info()
This function is used to show information about 4 of the biggest players when it comes to charging stations in Denmark. It simply asks for user's input to select for which company should the information be displayed. 

## Funtion location()
````
df = pd.read_csv('Charging_stations.csv', encoding='latin1', decimal= ',')
````
This function uses the library _Pandas_ to import the csv file and open it. We had to set the _encoding_ to _latin1_, because of the special caracters in the csv file. We also needed to change the values of longitude and latitude into floats, using the _.astype(float)_ function.

Afterwards, using the library _Folium_, we create a map object with a location in Copenhagen.
````
m = folium.Map(location= [55.6761, 12.5683], zoom_start=12)
````
To add charging stations markers on the map we used _For Loop_ funtion to go through each row of data in the csv and used folium's _folium.marker().add_to()_ function to add them to the map object. Since we wanted to create a visual differentiation between the stations based on the company, we used if and else statement that would assign different colors to markers based on the _row['operator']_. Using _FloatImage().add_to()_ we were able to append a legend(Legend.png). To generate the map, we used _.save()_ and subseqently used _webbrowser.open()_ to display it in your webbrowser.

## Function menu()
````
print(f"""\t\t
                ==================================================================
                |                                                                |
                |                       EC Chargers - Menu                       |
                |                                                                |
                ==================================================================
                |                                                                |
                |   1. Locate all possible charging stations                     |
                |   2. Get information about relevant specifications             |
                |      of a charger and charging fees                            |
                |   3. Check the status update on your charging                  |
                |   4. See the personal consumption                              |
                |   Press Q to quit this program                                 |
                |                                                                |
                ==================================================================
    """)
````
Just a visual menu created by using _print()_.

## While loop
To make sure that the menu will loop and doesn't end the program after one function. It asks for user's input to determine which function to call. Using the while loop we tell te code what to do for each part of the menu. If the user decides to see the map, all that is needed to do is just press 1 and the code will call the function location(). After each function of the menu is performed, the code asks for another user's input to decide whether to leave the program or choose different function in the menu.   


