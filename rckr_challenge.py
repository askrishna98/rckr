from math import radians, sin, cos, atan2, sqrt
import requests

data = requests.get(
    "https://cdn.jsdelivr.net/gh/apilayer/restcountries@3dc0fb110cd97bce9ddf27b3e8e1f7fbe115dc3c/src/main/resources/countriesV2.json").json()

population_limit=int(input("Enter population limit:- "))

# counting every currencies reoccurance and finds the exclusive unique currencies
count = {}
for country in data:
    for currency in country["currencies"]:
        count[currency["code"]] = count.get(currency["code"], 0)+1


# finding the details(coordinates and population) of countries which are satisfies the conditions
coordinates= {}
for country in data:
    if country["population"] >= population_limit:
        for currency in country["currencies"]:
            if count[currency["code"]] == 1:
                if len(country["latlng"])!=2:
                    coordinates[country["population"]] = [0.00,0.00]
                else:coordinates[country["population"]] = country["latlng"]

# sorting coordinates of countries according to population and takes first 20 out of them
coordinates=sorted(coordinates.items())[:20]

# function for getting length
def getlength(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi/2)**2 + \
        cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    length = 2*6371*atan2(sqrt(a), sqrt(1 - a))
    return round(length, 2)


# finds total length of all possible lines
total = float(0)
for i in range(len(coordinates)-1):
    for k in range(i+1,len(coordinates)):
        total += getlength(coordinates[i][1], coordinates[k][1])
print("Total length of all possible lines =",round(total, 2))
