# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time

# Import API key
# import api_keys

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# List for holding lat_lngs and cities
lat_lngs = []
cities = []
countries = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    near_country = citipy.nearest_city(lat_lng[0], lat_lng[1]).country_code
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)
        countries.append(near_country)

api_key = "ca948e37c7fc34fc07a1ece6ffdb31a0"

# Print the city count to confirm sufficient count
print(len(cities))


location_data = pd.DataFrame()
location_data['City'] = cities
location_data['Cloudiness'] = ""
location_data['Country'] = countries
location_data['Date'] = ""
location_data['Humidity'] = ""
location_data["Lat"] =""
location_data["Lng"] =""
location_data['Max Temp'] = ""
location_data['Wind Speed'] = ""

sample_size = 50
target_url = 'http://api.openweathermap.org/data/2.5/weather?q='
units = 'imperial'

print(location_data.head())


record = 0
for index, row in location_data.iterrows():
    city_name = row['City']
    country_code = row['Country']
    url = target_url + city_name + ',' + country_code + '&units=' + units + '&APPID=' + api_key
    print (url)
    try:
        weather_response = requests.get(url)
        weather_json = weather_response.json()
        latitude = weather_json["coord"]["lat"]
        longitude = weather_json["coord"]["lon"]
        temp = weather_json["main"]["temp"]
        humidity = weather_json["main"]["humidity"]
        cloud = weather_json["clouds"]["all"]
        wind = weather_json["wind"]["speed"]

        location_data.set_value(index, "Cloudiness", cloud)
        location_data['Date'] = ""
        location_data.set_value(index,"Humidity",humidity)
        location_data.set_value(index, "Lat", latitude)
        location_data.set_value(index, "Lng", longitude)
        location_data.set_value(index, "Max Temp", temp)
        location_data.set_value(index,"Wind Speed", wind)

        print("Processing Record %s of Set %s" % (np.mod(index,sample_size), np.int16(index/sample_size+1)))
    except:
        print('City not found. Skipping...')

    record += 1
    if record % 59 == 0:
        time.sleep(60)

#Export the city data into a .csv.
location_data.to_csv(output_data_file, encoding="utf-8", index=False)

#Display the DataFrame
colmnum_txt = list(location_data)
field_count = [[x,len(location_data)] for x in colmnum_txt]
print(field_count)
print(location_data.head())

#Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
location_data['Lat'] = pd.to_numeric(location_data['Lat'], errors = 'coerce')
location_data['Temp'] = pd.to_numeric(location_data['Max Temp'], errors = 'coerce')
location_data['Humidity'] = pd.to_numeric(location_data['Humidity'], errors = 'coerce')
location_data['Wind Speed'] = pd.to_numeric(location_data['Wind Speed'], errors = 'coerce')
location_data['Cloudiness'] = pd.to_numeric(location_data['Cloudiness'], errors = 'coerce')

#---------------------------------------------
# Axes values
x_axis = location_data['Lat']
y_axis = location_data['Max Temp']

plt.scatter(x_axis, y_axis, edgecolors='black')

plt.title("City Latitude vs. Max Temperature(08/22/18)")
plt.xlabel("Latitude")
plt.xlim(-60,90)
plt.ylabel("Max Temperature (F)")
plt.ylim(0,125)

#Save the plotted figures as .pngs.
plt.savefig("LatitudeVsTemperature.png")
plt.show()


# Axes values
x_axis = location_data['Lat']
y_axis = location_data['Humidity (%)']

plt.scatter(x_axis, y_axis, edgecolors='black', alpha=1)

plt.title("City Latitude vs. Humidity (08/22/18)")
plt.xlabel("Latitude")
plt.xlim(-60,90)
plt.ylabel("Humidity (%)")
plt.ylim(0,120)

plt.savefig("LatitudeVsHumidity.png")
plt.show()


# Axes values
x_axis = location_data['Lat']
y_axis = location_data['Cloudiness']

plt.scatter(x_axis, y_axis, edgecolors='black', alpha=1)

plt.title("City Latitude vs. Cloudiness (08/22/18)")
plt.xlabel("Latitude")
plt.xlim(-60, 90)
plt.ylabel("Cloudiness (%)")
plt.ylim(0, 120)

plt.savefig("LatitudeVsCloudiness.png")
plt.show()




