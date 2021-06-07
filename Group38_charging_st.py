import folium
from folium.plugins import FloatImage
import pandas as pd
import mysql.connector as sql
import time
import webbrowser
from time import sleep

# intro to the program
print(f"""\n\t\t 
      Welcome to a python program, which shows all possible charging stations for electric vehicles.
      Furthermore, it shows respective specifications about different charging stations, as well as gives
      the opportunity to see user's consumption and gives updates on current charging. 
      """)



# finding out if new or existing user
new_or_exist = input("\n\t\tAre you already registered in the database ? Please answer Yes or No: ")
new_or_exist = new_or_exist.title()


# creating a class to verify the login information and use functions based on the input above
# We did this because the functions inside the class are not the same for existing and new user
class Log_in():
    #create a database which will use mysql.connector to connect the code from python with mySQL
    #you might need to change this information since this is connecting it to my own MySQL connection
    __HOST= "localhost"
    __USERNAME= "root"
    __PASSWORD= "FilipFG7"
    __DATABASE= "exam2"

    def __init__(self,user_status):
        self.con = sql.connect(host=Log_in.__HOST,user=Log_in.__USERNAME,password=Log_in.__PASSWORD,database=Log_in.__DATABASE)
        self.user_status= user_status
    def veryfying(self):
        #depending if its a new user or not, the program will either log in the user or register him
        if new_or_exist == "Yes":
            #getting users info
            global existing_user_firstname
            existing_user_firstname = input("\n\t\tTo log into the program, please enter Your first name: ")
            existing_user_firstname = existing_user_firstname.title()
            
            global existing_user_secondname
            existing_user_secondname = input("\t\tPlease enter Your second name: ")
            existing_user_secondname = existing_user_secondname.title()
            
            #defining a cursor through which we will execute sql commands
            global mycursor
            mycursor = self.con.cursor()
            #defining a sql command, giving it the values that the user input
            check_login_info = "SELECT FirstName, LastName FROM EV_Owner WHERE FirstName = '%s' AND LastName = '%s'" % (existing_user_firstname, existing_user_secondname)
            #creating an empty list to append the values
            global login_credentials
            login_credentials= []
            try:
                #execute the command in sql
                mycursor.execute(check_login_info)
                
                
                #fetches the result from the select statement 
                result= mycursor.fetchall()
                #appending the result(values) into the empty list
                for row in result:
                    for x in row:
                        login_credentials.append(x)
            except:
                print("\t\tSomething went wrong. :(\n")
            # checking if the values already are in the database
            if (existing_user_firstname and existing_user_secondname) in login_credentials:
                print("\n\t\tHey! Welcome " + existing_user_firstname + " " + existing_user_secondname + " !\n")
            else:
                print("\n\t\tNo credentials found. Please double check the input information and try again.\n")

            

        else:
            print("\n\t\tLet's start with the registration. We will need Your first and last name, as well as Your Car model.")
            
            # mycursor is used to execute mysql statements
            mycursor = self.con.cursor()
            # getting info about new user
            global new_user_firstname
            new_user_firstname= input("\n\t\tPlease enter Your first name to register into the database: ")
            new_user_firstname= new_user_firstname.title()
            global new_user_secondname
            new_user_secondname= input("\t\tPlease enter Your second name: ")
            new_user_secondname= new_user_secondname.title()
            
            # insert statements stored in variables
            add_new_user= "INSERT INTO EV_Owner (FirstName, LastName) VALUES (%s, %s);"
           
            #info of the new user is stored in a tuple
            global data_new_user
            data_new_user = (new_user_firstname, new_user_secondname)

            #insert new user 
            mycursor.execute(add_new_user, data_new_user)
            
            # get the ownerID value with mycursor.lastrowid
            global OwnerID2
            OwnerID2 = mycursor.lastrowid
            self.con.commit()

            # info about the car
            global new_user_car
            new_user_car= input("\t\tPlease enter Your car model: ")
            new_user_car= new_user_car.title()
            add_new_user_car= "INSERT INTO Car (Model, OwnerID) VALUES (%s, %s); "

            #info about the car is stored in a tuple
            global data_new_car
            data_new_car = (new_user_car, OwnerID2)
            global CarID
            CarID= mycursor.lastrowid
            #insert new car
            mycursor.execute(add_new_user_car, data_new_car)
            self.con.commit()
            
            #let the user know that his login credentials are store in the database
            print("\n\t\tPerfect! We have stored Your data in the database. Welcome "+ new_user_firstname + " "+new_user_secondname+ " !\n\t\t We hope that You will enjoy our program! :)\n" )
   
    # function within class to check the consumption of the user
    def check_consumption(self):
        if new_or_exist == "Yes":
            
            # create a script that will be run in mysql
            ownerid_consumpt_script="SELECT OwnerID FROM EV_Owner WHERE FirstName = '%s' AND LastName = '%s'" % (existing_user_firstname, existing_user_secondname)
            # create a list to store the values           
            OwnerID_consumpt=[]
            

            # execute the script 
            mycursor.execute(ownerid_consumpt_script)
            owner_result= mycursor.fetchone()
            
            # append the result from the select statement into the list above
            for x in owner_result:
                OwnerID_consumpt.append(x)
            
            # change the ownerID_consumpt list into an integer 
            owner_string = [str(integer) for integer in OwnerID_consumpt]
            owner_string2 = "".join(owner_string)
            global integer_owner
            integer_owner = int(owner_string2)
                
            # use the integer to get the personal consumption for the user, using a mysql command
            consumption_sql_script= "SELECT Personal_consumption FROM charging_status WHERE OwnerID = '%s'" % (integer_owner)
            consumption_data= []
            
            # create a loop statement that will append the selected data into the list above
            try:
                mycursor.execute(consumption_sql_script)
                consump_result= mycursor.fetchall()
                for row in consump_result:
                    for x in row:
                        consumption_data.append(x)
            except:
                print("\t\tSomething went wrong.")

            # change the consumption_data list into an integer
            consumption_string = [str(integer) for integer in consumption_data]
            global consumption_string2
            consumption_string2 = "".join(consumption_string)
            
            # even though we dont use the integer in this function
            # that's also why we made it a global variable
            global integer_consumption
            integer_consumption = int(consumption_string2)
            
        else:
            try:
                # create a script that will be run in mysql
                new_ownerid_consumpt_script="SELECT OwnerID FROM EV_Owner WHERE FirstName = '%s' AND LastName = '%s'" % (new_user_firstname, new_user_secondname)
                # create a list to store the values           
                new_OwnerID_consumpt=[]
                

                # execute the script 
                mycursor.execute(new_ownerid_consumpt_script)
                new_owner_result= mycursor.fetchone()
                
                # append the result from the select statement into the list above
                for x in new_owner_result:
                    new_OwnerID_consumpt.append(x)
                
                # change the ownerID_consumpt list into an integer 
                new_owner_string = [str(integer) for integer in new_OwnerID_consumpt]
                new_owner_string2 = "".join(new_owner_string)
                global integer_new_owner
                integer_new_owner = int(new_owner_string2)
                    
                # use the integer to get the personal consumption for the user, using a mysql command
                newuser_consumption_sql_script= "SELECT Personal_consumption FROM charging_status WHERE OwnerID = '%s'" % (integer_new_owner)
                newuser_consumption_data= []
                
                # create a loop statement that will append the selected data into the list above
                try:
                    mycursor.execute(newuser_consumption_sql_script)
                    newuser_consump_result= mycursor.fetchall()
                    for row in newuser_consump_result:
                        for x in row:
                            newuser_consumption_data.append(x)   
                except:
                    print("\t\t Something went wrong.") 
                
                # change the consumption_data list into an integer
                newuser_consumption_string = [str(integer) for integer in newuser_consumption_data]
                global newuser_consumption_string2
                newuser_consumption_string2 = "".join(newuser_consumption_string)
                
                # even though we dont use the integer in this function
                # that's also why we made it a global variable
                global newuser_integer_consumption
                newuser_integer_consumption = int(newuser_consumption_string2)
            except:
                print("\n")


    # function within the class to check the status update on the charging
    def status_update(self):
        if new_or_exist == "Yes":
            # get an input from the existing user and change it to an integer so that we can use it in addition
            charging_time= input("\n\t\tHow long would You like to charge Your car for? Please state in minutes: ")
            charging_time_int= int(charging_time)
            
            # add the new charging time to the personal consumption
            new_consumption = charging_time_int + integer_consumption
            # change the integer to string so we can display it in print
            new_consumpt_str= str(new_consumption)
           
            update_consumption_script= "UPDATE charging_status SET Personal_consumption= '%s' WHERE OwnerID= '%s'" %(new_consumption, integer_owner)
            mycursor.execute(update_consumption_script)

            #save the cahnges in the mysql table
            self.con.commit()

            print("\n\t\tGreat! You will be notified when Your charging is done! ")
            # the function sleep is imitating the charging time, since there is not an actual charging happening
            sleep(5)
            print("\n\t\tYour charging is done! Your personal consumption has been updated. New personal consumption: " +new_consumpt_str+ " minutes\n")


        else:
            # get an input from the new user and change it to integer
            charging_time_new= input("\n\t\tHow long would You like to charge Your car for? Please state in minutes: ")
            charge_time_new_int= int(charging_time_new)
            
            #script to run in mysql
            newuser_consumpt_script= "INSERT INTO charging_status (Personal_Consumption, OwnerID, CarID, Remaining_time, StationID) Values (%s, %s, %s, %s, %s); "
            # store all the data into one variable. Remaining time and stationID had to be added like this
            # because we have no way of accessing the data from the actual charging station, because we do not actually have a car charging there. Therefore, we simulate it this way.
            newuser_data= (charge_time_new_int, OwnerID2, CarID, "0", "node/4494319276")

            # execute the script with selected data. 
            mycursor.execute(newuser_consumpt_script, newuser_data)
            #save it to the mysql table
            self.con.commit()
            print("\n\t\tGreat! You will be notified when Your charging is done! ")
            # the function sleep is imitating the charging time, since there is not an actual charging happening
            sleep(5)
            print("\n\t\tYour charging is done! Your personal consumption has been updated. New personal consumption: " +charging_time_new+ " minutes\n")


global user
user = Log_in(new_or_exist)
user.veryfying()


#function that will display specifications about respective company
def info():
    print(f"""\n\t\t

        Find out about the specifications of the chargers. We have information about 4 of the biggest players in this industry:
        E-ON, Clever, Tesla, Sperto.

    """)
    charger_specs = input("\n\t\tWhich supplier of charging stations would you like to know more about ? : ")
    charger_specs = charger_specs.upper()

    if charger_specs == "CLEVER":
        print(f"""\n\t\t

        CLEVER chargers are spread out across the whole Denmark. All of Clever's public network chargers have an effect of at least 22kWh. 
        Clever chargers have different plug types: Type-2 AC 43kW, Type-2 AC 11-22kW, CHAdeMO DC 50kW, CCS DC 50 kW. 
        For more information about the different types of plugs, check out this webpage: https://www.zap-map.com/charge-points/connectors-speeds/ 
        
        The price for charging with Clever's chargers starts at 3,5 DKK per kWh for normal charging, and 5DKK per kWh for ultra-fast charging. 
        For more information you can visit their webpage: https://clever.dk/
        
        """)
        
        
    elif charger_specs == "E-ON":
        print(f"""

        E-ON chargers are mostly situated inside and around big cities. E-ON has 1,600 public charging spots with electricity from renewable energy sources.
        Fast E-ON chargers support different plug types: Type-2, CHAdeMO and CCS. 
        For more information about the different types of plugs, check out this webpage: https://www.zap-map.com/charge-points/connectors-speeds/
        
        The price for charging with E-ON's chargers is 5.55 DKK per kWh. 
        For more information you can visit their webpage: https://www.eon.dk/privat.html

        """)
        
    elif charger_specs == "TESLA":
        print(f"""

        Tesla chargers are spread out throughout the whole Denmark and its neighbouring countries. 
        In order to use the Tesla chargers without having a Tesla EV, one will have to use an adapter the Tesla to J1772 connector.

        The price for charging with Tesla chargers starts at approximately 2,55 DKK per kWh.
        For more information you can visit their webpage: https://www.tesla.com/da_DK/charging

        """)
        
    elif charger_specs == "SPERTO":
        print(f"""

        The price for charging with Sperto's chargers can start at 1DKK per kWh. When you buy a charging box, you will pay approximately 2DKK per kWh.
        If you rent a charging box, you will pay 75DKK per month for the box plus approximately 1DKK per kWh. 
        Another option is to pay fixed montly subscription, which is around 750-800 DKK.
        For more information you can visit their website: https://www.sperto.dk/

        """)
        
    else:
        print("\n\t\tHave a nice day!\n")
        exit()


#function that will create a map with charging stations as markers, with a legend explaining the color difference of markers
def location():
    #import csv file using pandas, set encoding to latin1 because of the special characters in csv file
    df = pd.read_csv('Charging_stations.csv', encoding='latin1', decimal= ',')
    df.head()
    #change the values from string to float
    df["latitude"]= df["latitude"].astype(float)
    df['longitude']= df['longitude'].astype(float)

    # create map object with location in Copenhagen
    m = folium.Map(location= [55.6761, 12.5683], zoom_start=12)

    # import csv file with charging stations locations into map
    for index, row in df.iterrows():
        label = "{}, {}".format(row['id'],row['operator'])
        popup= label
        if row['operator'] == "Tesla Motors Inc.":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="blue",icon="bolt", prefix='fa')
                        ).add_to(m)   
        elif row['operator'] == "Tesla":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="blue",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "Clever":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="green",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "Sperto":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="orange",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "E-On":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="red",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "Eon":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="red",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "E.ON":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="red",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "e.On":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="red",icon="bolt", prefix='fa')
                        ).add_to(m)                 
        elif row['operator'] == "e-on":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="red",icon="bolt", prefix='fa')
                        ).add_to(m)
        elif row['operator'] == "eon":
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="red",icon="bolt", prefix='fa')
                        ).add_to(m)
        else:
            folium.Marker(
            location=[row['latitude'], row['longitude']],
                    popup= popup,
                        icon=folium.Icon(color="darkpurple",icon="bolt", prefix='fa')
                        ).add_to(m)

    # add legend picture as floatimage
    FloatImage('Legend.png', bottom=70, left=86).add_to(m)



    # Generate map and use the library webbrowser to open the map
    m.save('map.html')
    webbrowser.open("map.html ")
    



#create a menu that will be used to select what the program should do
def menu():

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

loop = True
menu()
#create a while loop statement, throguh which we put the menu in a loop until the user decides to leave the program
while loop:
    choice= input("\n\t\tWhat would You want this program to do? Simply type the number of the function that You would wish to use: ")

    if choice== "1":
        location()
        menu_or_out = input("\n\t\tIf you want to go back to the menu, press Y. If you want to quit, press Q: ")
        menu_or_out = menu_or_out.upper()
        if menu_or_out == "Y":
            menu()
        else:
            exit()

    elif choice== "2":
        info()
        menu_or_out2 = input("\n\t\tIf you want to go back to the menu, press Y. If you want to quit, press Q: ")
        menu_or_out2 = menu_or_out2.upper()
        if menu_or_out2 == "Y":
            menu()
        else:
            exit()


    elif choice== "3":
        user.check_consumption()
        user.status_update()
        
        menu_or_out3 = input("\n\t\tIf you want to go back to the menu, press Y. If you want to quit, press Q: ")
        menu_or_out3 = menu_or_out3.upper()
        if menu_or_out3 == "Y":
            menu()
        else:
            exit()

    elif choice== "4":
        if new_or_exist == "Yes":
            user.check_consumption()
            print("\n\t\tYour personal consumption up to this point is : " +consumption_string2)
            menu_or_out4 = input("\n\t\tIf you want to go back to the menu, press Y. If you want to quit, press Q: ")
            menu_or_out4 = menu_or_out4.upper()
            if menu_or_out4 == "Y":
                menu()
            else:
                exit()
        else:
            user.check_consumption()
            print("\n\t\tYour personal consumption up to this point is : " +newuser_consumption_string2)
            menu_or_out5 = input("\n\t\tIf you want to go back to the menu, press Y. If you want to quit, press Q: ")
            menu_or_out = menu_or_out5.upper()
            if menu_or_out5 == "Y":
                menu()
            else:
                exit()
    else:   
        print("\n\t\tHave a nice day!")


