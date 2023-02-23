from bs4 import BeautifulSoup
import requests
import pandas as pd 
from math import ceil

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

state = input("Enter Name of State shortened\n For example, New York would be NY: ")
state = state.capitalize()
city = input("Enter full name of city: ")

WEBSITE = 'https://www.trulia.com/%(state)s/%(city)s/' % {"state": state.capitalize(), "city" : city }

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})

response = requests.get(WEBSITE, headers = headers)

real_estate = pd.DataFrame(columns = ['Address', 'Beds', 'Baths', 'Price'])

soup = BeautifulSoup(response.content, 'html.parser')

total_homes = soup.find('h2', {'class':'SearchResultsHeadings__ResultCountText-sc-1npyos5-1 gRoetB'})
total_homes = total_homes.text.strip(' homes')
total_homes = int(total_homes.replace(',', ''))
total_homes = ceil(total_homes/40) #Divide by 40, since that is the amount per page.


for i in range(1, 10, 1): #10 is here so I can run the program without waiting a century. Feel free to change it to the value of total_homes or a random integer.
    try:
        if i == 1:
            website = WEBSITE
        else:
            website = WEBSITE + str(i) +'_p/'

        headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})

        response = requests.get(website, headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        result_update = soup.find_all('li', {'class' : 'Grid__CellBox-sc-144isrp-0 SearchResultsList__WideCell-sc-14hv67h-2 gBXIcq bmFlVd'})

        address = []
        beds = []
        baths = []
        prices = []

        for result in result_update:
            bed = result.find('div', {'data-testid':'property-beds'})
            bath = result.find('div', {'data-testid':'property-baths'})
            addy = result.find('div', {'data-testid':'property-address'})
            price = result.find('div', {'data-testid': 'property-price'})
            squarefoot =  result.find('div', {'data-testid': 'property-floorSpace'})

            if bed != None and bath != None:
                bed = bed.text.strip()
                bath = bath.text.strip()
                baths.append(bath)
                beds.append(bed)
            elif bed != None and bath == None:
                bed = bed.text.strip()
                baths.append(0)
                beds.append(bed)
            elif bed == None and bath != None:
                bath = bath.text.strip()
                beds.append(0)
                baths.append(bath)
            if addy != None:
                addy = addy.text.strip()
                address.append(addy)
            if price != None:
                price = price.text.strip()
                prices.append(price)
                print(price)
            

        


    except:
        continue
        # print (i)

    # for i in range(len(address)):

    for i in range (len(address)):
        try:
            real_estate=real_estate.append({'Address':address[i], 'Beds':beds[i], 'Baths':baths[i], 'Price':prices[i]}, ignore_index=True)
        except:
            continue

real_estate.to_csv('real restate.csv')
