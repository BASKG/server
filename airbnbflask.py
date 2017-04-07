import flask
from flask import request
from flask_cors import CORS, cross_origin
import requests
import json
app = flask.Flask(__name__)
CORS(app)

#-------- MODEL GOES HERE -----------#
import numpy as np
import pandas as pd

#-------- ROUTES GO HERE -----------#
@app.route('/predict', methods=['GET','POST'])
@cross_origin()
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':
        listing =  request.form['listing']
        if len(listing) > 10:
            m = re.search("/rooms/(\d+)", listing)
            listing = m.group[1]
        PREDICTOR = pd.read_pickle('model')

        cats = ['host_is_superhost',  'host_has_profile_pic',  'host_identity_verified',  'zipcode',  'property_type',  'room_type',\
         'accommodates',  'bathrooms',  'bedrooms',  'beds',  'bed_type',  'amenities',  'price',  'number_of_reviews',  'review_scores_accuracy',\
         'review_scores_cleanliness',  'review_scores_checkin',  'review_scores_communication', 'review_scores_location',  'review_scores_value',  'instant_bookable',\
         'cancellation_policy']

        amenities = ['Other pet(s)', 'Essentials', 'Doorman Entry', 'Fire extinguisher', 'Suitable for events', 'Gym', 'Air conditioning', 'translation missing: en.hosting_amenity_50',\
         'Internet', 'Washer', 'Hangers', 'Laptop friendly workspace', 'Smoking allowed', 'TV', 'Cat(s)', 'Indoor fireplace', 'Hair dryer', 'First aid kit',\
         'translation missing: en.hosting_amenity_49', 'Cable TV', 'Smoke detector', 'Free parking on street', 'Private living room', '24-hour check-in', 'Washer / Dryer',\
         'Family/kid friendly', 'Carbon monoxide detector', 'Pets allowed', 'Shampoo', 'Heating', 'Wheelchair accessible', 'Smartlock', 'Iron', 'Self Check-In',\
         'Free parking on premises', 'Pets live on this property', 'Buzzer/wireless intercom', 'Doorman', 'Keypad', 'Hot tub', 'Dryer', 'Lock on bedroom door',\
         'Elevator in building', 'Private entrance', 'Dog(s)', 'Wireless Internet', 'Pool', 'Breakfast', 'Kitchen', 'Safety card', 'Lockbox']

        proptypes = ['House', 'Apartment', 'Boat', 'Townhouse', 'Dorm', 'Condominium',\
           'Other', 'Bed & Breakfast', 'Loft', 'Guesthouse', 'Hostel',\
           'Bungalow', 'Boutique hotel', 'Serviced apartment', 'Villa',\
           'Timeshare', 'Cabin', 'Earth House', 'Cave', 'Castle', 'Hut',\
           'Island', 'Chalet']
        proptypes.sort()

        bedtypes = ['Real Bed', 'Couch', 'Futon', 'Pull-out Sofa', 'Airbed']

        canpols = ['flexible','moderate', 'strict', 'super_strict_30']

        roomtypes = ['Entire home/apt', 'Private room', 'Shared room']

        url = 'https://api.airbnb.com/v2/listings/' + str(listing) + '?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US&currency=USD&_format=v1_legacy_for_p3&_source=mobile_p3'
        r = requests.get(url)
        lis = r.json()['listing']

        his = lis['primary_host']['is_superhost']
        hhpp = lis['primary_host']['has_profile_pic']
        hiv = lis['primary_host']['identity_verified']
        zipcode = lis['zipcode']
        pt = lis['property_type']
        rt = lis['room_type']
        acc = lis['person_capacity']
        bath = lis['bathrooms']
        bedr = lis['bedrooms']
        beds = lis['beds']
        bedt = lis['bed_type']
        amn = lis['amenities']
        price = lis['price']
        nrev = lis['reviews_count']
        rsa = lis['review_rating_accuracy']
        rscl = lis['review_rating_cleanliness']
        rsch = lis['review_rating_checkin']
        rsco = lis['review_rating_communication']
        rsl = lis['review_rating_location']
        rsv = lis['review_rating_value']
        ib = lis['instant_bookable']
        cp = lis['cancellation_policy']



        columns = ['host_is_superhost',
        'host_has_profile_pic',
        'host_identity_verified',
        'zipcode',
        'accommodates',
        'bathrooms',
        'bedrooms',
        'beds',
        'price',
        'number_of_reviews',
        'review_scores_accuracy',
        'review_scores_cleanliness',
        'review_scores_checkin',
        'review_scores_communication',
        'review_scores_location',
        'review_scores_value',
        'instant_bookable',
        'Other pet(s)',
        'Essentials',
        'Doorman Entry',
        'Fire extinguisher',
        'Suitable for events',
        'Gym',
        'Air conditioning',
        'translation missing: en.hosting_amenity_50',
        'Internet',
        'Washer',
        'Hangers',
        'Laptop friendly workspace',
        'Smoking allowed',
        'TV',
        'Cat(s)',
        'Indoor fireplace',
        'Hair dryer',
        'First aid kit',
        'translation missing: en.hosting_amenity_49',
        'Cable TV',
        'Smoke detector',
        'Free parking on street',
        'Private living room',
        '24-hour check-in',
        'Washer / Dryer',
        'Family/kid friendly',
        'Carbon monoxide detector',
        'Pets allowed',
        'Shampoo',
        'Heating',
        'Wheelchair accessible',
        'Smartlock',
        'Iron',
        'Self Check-In',
        'Free parking on premises',
        'Pets live on this property',
        'Buzzer/wireless intercom',
        'Doorman',
        'Keypad',
        'Hot tub',
        'Dryer',
        'Lock on bedroom door',
        'Elevator in building',
        'Private entrance',
        'Dog(s)',
        'Wireless Internet',
        'Pool',
        'Breakfast',
        'Kitchen',
        'Safety card',
        'Lockbox','property_type', 'room_type', 'bed_type', 'cancellation_policy']

        amne = []
        for i in amenities:
            if i in amn:
                amne.append(1)
            else:
                amne.append(0)

        props = []
        for i in proptypes:
            if i in pt:
                props.append(1)
            else:
                props.append(0)

        roomt = []
        for i in roomtypes:
            if i in rt:
                roomt.append(1)
            else:
                roomt.append(0)

        bt = []
        for i in bedtypes:
            if i in bedt:
                bt.append(1)
            else:
                bt.append(0)

        canp = []
        for i in canpols:
            if i in cp:
                canp.append(1)
            else:
                canp.append(0)


        item = [his,hhpp,hiv,int(zipcode),acc,bath,bedr,beds,nrev,rsa,rscl,rsch,rsco,rsl,rsv,ib]
        item.extend(amne)
        item.extend(props)
        item.extend(roomt)
        item.extend(bt)
        item.extend(canp)
        item = np.array(item)
        score = PREDICTOR.predict(item.reshape(1, -1))[0]
        results = {'predicted_price': score, 'actual_price': lis['price']}
        return json.dumps(results)

if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
