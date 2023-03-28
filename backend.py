import requests
import pprint as pp
from datetime import datetime, timedelta

# TODO: To EMAIL data to user and GUI.
'''
REQUIRED DETAILS

locale: DONE
fly_from: DONE
fly_to: DONE
date_from: DONE
date_to: DONE
flight_type -> oneway/return : DONE
return_from: DONE
return_to: DONE
selected_cabins: DONE
currency: DONE
price_from: DONE
price_to: DONE

NUMBER OF ADULTS, CHILDREN, INFANTS

# EXAMPLE OF REQUEST URL
# https://api.tequila.kiwi.com/v2/search?fly_from=FRA&fly_to=PRG&date_from=01%2F04%2F2023&date_to=05%2F04%2F2024&flight_type=oneway&one_for_city=0&one_per_date=0&partner_market=us&price_from=0&price_to=500&vehicle_type=aircraft&limit=5
'''


# 1 - TO ASK THE USER FOR THE SOURCE AND DESTINATION AND FIND ITS DATA.
# 2 - USE THE API TO GET IATA CODES AND OTHER DATA OF FLY-FROM AND FLY-TO.
# 3 - TO ASK FOR EXTRA DETAILS LIKE MAX_STOP-OVERS + NO_OF_PEOPLE + CHILDREN-SIBLINGS-ELDERLY + CABIN-CLASS.
# 4 - And then format data and use it to find the flight data.

def find_loc_data(source: str, destination: str, source_country: str, destination_country: str):
    places = (source, destination)
    country_dict = {
        source: source_country.lower(),
        destination: destination_country.lower()
    }
    search_url = 'https://api.tequila.kiwi.com/locations/query'
    search_headers = {'apikey': 'OL_rv10MTqCcfcWJ6rXEPg7Qst-JXODA'}

    final_response = []

    for place in places:

        country = country_dict[place]
        country_found = False
        search_params = {
            'term': place,
            'locale': 'en-US',
            'location_types': 'airport',
            'limit': 10,
            'active_only': 'true'
        }

        response = requests.get(url=search_url, params=search_params, headers=search_headers)
        response.raise_for_status()
        body = response.json()
        loc: list = body['locations']

        if len(loc) == 0:
            exp_str = f'{place.title()},{country.title()} WAS NOT FOUND!'
            raise Exception(exp_str)

        for every_loc in loc:
            loc_country = every_loc['city']['country']['name'].lower()
            if loc_country == country:
                country_found = True
                loc_data = {
                    'id': every_loc['id'],
                    'airport_name': every_loc['name'],
                    'city_id': every_loc['city']['id'],
                    'city_name': every_loc['city']['name'],
                    'country_id': every_loc['city']['country']['id'],
                    'country_name': every_loc['city']['country']['name'],
                    'region_id': every_loc['city']['region']['id'],
                    'region_name': every_loc['city']['region']['name'],
                }
                final_response.append(loc_data)

        if not country_found:
            exp_str = f'{place.title()},{country.title()} WAS NOT FOUND!'
            raise Exception(exp_str)

    return final_response


# user_email = input('PLEASE ENTER YOUR EMAIL-ID : ')
# user_email_valid = True if user_email else False


def ask_flight_details(iata_from: str, iata_to: str):
    date_from: str
    date_to: str
    return_from: str
    return_to: str
    selected_cabins: str
    price_from: int
    price_to: int
    curr: str
    max_stopovers: int
    adults: int
    children: int
    infants: int

    locale = 'en'

    flight_type_ip = int(input('\nCHOOSE THE FLIGHT TYPE.\n1)ONEWAY\n2)ROUND-TRIP\nEnter Your Choice : '))
    while flight_type_ip not in [1, 2]:
        flight_type_ip = int(input('CHOOSE A VALID FLIGHT TYPE 1)ONEWAY 2)ROUND-TRIP\nEnter Your Choice : '))
    flight_type = 'oneway' if flight_type_ip == 1 else 'round'

    date_from = datetime.now().strftime('%d/%m/%Y')
    date_to = (datetime.now() + timedelta(days=180)).strftime('%d/%m/%Y')

    cabin_dict = {'M': 'economy', 'W': 'economy premium', 'C': 'business', 'F': 'first class'}
    print('\nCHOOSE THE CABIN-TYPE YOU WANT TO BOOK ,')
    for cabin in cabin_dict:
        print(f'{cabin} : {cabin_dict[cabin].title()}')
    selected_cabins = input('ENTER THE CABIN CODE : ').upper()
    while selected_cabins not in cabin_dict.keys():
        selected_cabins = input('ENTER A VALID CABIN CODE : ').upper()

    currencies = ['USD', 'INR', 'GBP']
    print('\nSELECT A CURRENCY TO PAY FOR FLIGHT,')
    for c in currencies:
        print(f'{currencies.index(c) + 1}) {c}')
    curr_index = int(input('CHOOSE A CURRENCY : ')) - 1
    while curr_index not in range(len(currencies)):
        curr_index = int(input('CHOOSE A VALID CURRENCY : ')) - 1
    curr = currencies[curr_index]

    price_from = int(input('\nENTER YOUR BASE PRICE FOR THE FLIGHT DEAL : '))
    price_to = int(input('ENTER YOUR MAX PRICE FOR THE FLIGHT DEAL : '))

    stop_overs = input('\nWOULD YOU LIKE TO HAVE STOP-OVERS ?? (y/n) : ').lower()
    while stop_overs not in ['y', 'n', 'yes', 'no']:
        stop_overs = input('ENTER VALID OPTION => (y/n) : ').lower()
    if stop_overs in ['y', 'yes']:
        max_stopovers = int(input('ENTER THE MAXIMUM NUMBER OF STOP-OVERs YOU WOULD LIKE TO HAVE , RANGE(1-9) : '))
        while max_stopovers not in range(1, 10):
            max_stopovers = int(input('ENTER VALID NUMBER OF STOP-OVERs YOU WOULD LIKE TO HAVE , RANGE(1-9) : '))
    else:
        max_stopovers = 0

    final_dict = {
        'fly_from': iata_from,
        'fly_to': iata_to,
        'locale': locale,
        'date_from': date_from,
        'date_to': date_to,
        'selected_cabins': selected_cabins,
        'curr': curr,
        'price_from': price_from,
        'price_to': price_to,
        'max_stopovers': max_stopovers,
        'limit': 7
    }

    if flight_type == 'round':
        return_from = (datetime.now() + timedelta(days=14)).strftime('%d/%m/%Y')
        return_to = (datetime.now() + timedelta(days=180)).strftime('%d/%m/%Y')
        final_dict['return_from'] = return_from
        final_dict['return_to'] = return_to

    return final_dict


def print_deal_data(deal_data: list):
    all_deals = {}

    for idx, deal in enumerate(deal_data):
        details = {
            'airlines': deal['airlines'],
            'seats_availability': deal['availability']['seats'] if deal['availability']['seats'] is not None else 0,
            'cityCodeFrom': deal['cityCodeFrom'],
            'cityFrom': deal['cityFrom'],
            'cityCodeTo': deal['cityCodeTo'],
            'cityTo': deal['cityTo'],
            'countryFromCode': deal['countryFrom']['code'],
            'countryFromName': deal['countryFrom']['name'],
            'countryToCode': deal['countryTo']['code'],
            'countryToName': deal['countryTo']['name'],
            'fare': deal['fare'],
            'link': deal['deep_link'],
            'duration': deal['duration'],
            'facilitated_booking_available': deal['facilitated_booking_available'],
            'local_arrival': deal['local_arrival'],
            'local_departure': deal['local_departure'],

        }
        all_deals[idx] = details

    for deal in all_deals.values():
        if deal['seats_availability'] != 0:
            pp.pprint(deal)
            print('\n\n')


def find_flight(place_from: str, place_to: str):
    main_url = 'https://api.tequila.kiwi.com/v2/search'
    search_headers = {'apikey': 'OL_rv10MTqCcfcWJ6rXEPg7Qst-JXODA'}

    param_dict = ask_flight_details(place_from, place_to)

    response = requests.get(url=main_url, params=param_dict, headers=search_headers)
    response.raise_for_status()
    json_response = response.json()
    flight_data: list = json_response['data']
    # pp.pprint(flight_data)
    if len(flight_data) == 0:
        print('No Flight Deal Found.')
    else:
        print_deal_data(deal_data=flight_data)


'''
if find_loc_data() => success
    then do ask_flight_details()
'''
if __name__=='__main__':
    fly_from = input('ENTER YOUR FLY-FROM / SOURCE PLACE/AIRPORT NAME/CODE : ')
    fly_from_country = input('ENTER YOUR FLY-FROM / SOURCE COUNTRY NAME : ')
    fly_to = input('ENTER YOUR FLY-TO / DESTINATION PLACE/AIRPORT NAME/CODE : ')
    fly_to_country = input('ENTER YOUR FLY-TO / DESTINATION COUNTRY NAME : ')

    try:
        loc_results = find_loc_data(
            source=fly_from,
            destination=fly_to,
            source_country=fly_from_country,
            destination_country=fly_to_country
        )
        find_flight(place_from=loc_results[0]['id'], place_to=loc_results[1]['id'])
    except Exception as e:
        print(e)