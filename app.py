from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
import requests
import pprint
import math
import os

load_dotenv()
key = os.getenv('KEY')

app = Flask(__name__)


@app.route('/')
def test():
    return render_template('map.html', key=key)


@app.route('/getRoutes', methods=['GET'])
def getRoutes():
    print(request.args)
    source = request.args.get('source')
    destination = request.args.get('destination')
    source.replace(' ', '+')
    destination.replace(' ', '+')
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+source + \
        '&destination='+destination+'&sensor=false&alternatives=true&mode=driving&key='+key
    r = requests.get(url)
    r = r.text
    d = eval(r)
    print(d)
    d['routes'] = d['routes'][0:1]
    return jsonify(d)


@app.route('/findsafety', methods=['POST'])
def findsafety():
    data = request.json
    path = data['routes']
    rearranged, extra = safety(path)
    routes = [0]*len(rearranged)
    for i in range(len(rearranged)):
        routes[i] = data['routes'][rearranged[i]]
    data['routes'] = routes
    bDi = {'data': data, 'extra': extra}
    return jsonify(bDi)


def safety(paths):
    print("#Routes :", len(paths))
    factors = ["bakery", "bank", "beauty_salon", "bicycle_store", "book_store", "cafe", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist", "department_store", "doctor", "electronics_store", "fire_station", "florist", "furniture_store", "gas_station", "home_goods_store",
               "hospital", "jewelry_store", "library", "local_government_office", "lodging", "movie_theater", "pet_store", "pharmacy", "police", "post_office", "restaurant", "school", "shoe_store", "shopping_mall", "stadium", "subway_station", "supermarket", "synagogue", "train_station", "transit_station", "zoo"]
    index = []
    Places = []
    count = 0
    best = []
    for route in paths:
        path = route['overview_path']
        for i in range(0, len(path), 7):
            lat = path[i]['lat']
            lng = path[i]['lng']
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + \
                str(lat)+","+str(lng)+"&radius=100&type="
            for factor in factors:
                url += str(factor)+","
            url = url[:-1]
            url += "&key="+key+"&opennow=true"
            r = requests.get(url)
            places = r.json()
            for place in places['results']:
                for factor in place['types']:
                    if factor in factors:
                        Places.append(place)
                        break
        index.append([0 for i in range(len(path))])
        best2 = []
        for i in range(len(path)):
            l = []
            for place in Places:
                x = place['geometry']['location']['lat']
                y = place['geometry']['location']['lng']
                x1 = path[i]['lat']
                y1 = path[i]['lng']
                #print(math.sqrt((x-x1)**2 + (y-y1)**2)*111319.444444)
                if math.sqrt((x-x1)**2 + (y-y1)**2)*111319.444444 <= 50:
                    l.append(place)
                    index[-1][i] += 1
            best2.append(l)
        best.append(best2)
    rearranged = arrangement(index)
    print(index)
    return rearranged, best[rearranged[0]]


def arrangement(index):
    # mxsf : max so far
    # lc : least count. longest sequence of the least number
    l = [i for i in range(len(index))]
    for j in range(len(index)-1):
        for i in range(len(index)-j-1):
            if min(index[l[i]]) < min(index[l[i+1]]):
                l[i], l[i+1] = l[i+1], l[i]
            elif min(index[l[i]]) == min(index[l[i+1]]):
                mv = min(index[l[i]])
                lc = [0, 0]
                mxsf = 0
                for k in range(2):
                    for e in index[l[i+k]]:
                        if e == mv:
                            mxsf += 1
                        else:
                            lc[k] = mxsf if mxsf > lc[k] else lc[k]
                            mxsf = 0
                    lc[k] = mxsf if mxsf > lc[k] else lc[k]
                if lc[0] > lc[1]:
                    l[i], l[i+1] = l[i+1], l[i]
                elif lc[0] == lc[1]:
                    counts = [0, 0]
                    for k in range(2):
                        for e in index[l[i+k]]:
                            if e == mv:
                                counts[k] += 1
                    if counts[0] > counts[1]:
                        l[i], l[i+1] = l[i+1], l[i]
    print(l)
    return l


@app.route('/sos', methods=['POST'])
def sos():
    data = request.json
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + \
        str(data['lat'])+','+str(data['lng'])+'&key='+key
    resp = requests.get(url)
    d = resp.json()
    print(d)
    addr = d['results'][0]['formatted_address']
    url = 'https://www.fast2sms.com/dev/bulk'
    print(data)
    numl = []
    for i in range(1, 4):
        if data['emc'+str(i)] != '':
            numl.append(data['emc'+str(i)])
    nums = ','.join(numl)
    print(nums)
    params = {
        'sender_id': 'FSTSMS',
        'message': 'ALERT\nYou are getting this message because your friend '+data['username']+' sent an SOS signal.\nTheir location is: '+addr,
        'numbers': nums,
        'language': 'english',
        'route': 'p'
    }
    resp = requests.post(url, data=params, headers={
                         'authorization': 'qe0xOBau29VkSQDdHmcFKX8forMGwj5gRtyPiNhpZJlE4UW6bYuP5pnKdFJX4q7WYQhf3HR61iGxCNzI'})
    # print(resp.text)
    print(data)
    return jsonify(data)


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('.', path)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
