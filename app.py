from flask import Flask, request, jsonify, render_template
import requests,pprint
app = Flask(__name__,template_folder=".")
key = 'AIzaSyCxb7VjOyG0RqazuliBkyZlP3h437hshkk'

@app.route('/')
def test():
    return render_template('test.html')
    
@app.route('/getRoutes', methods=['GET'])
def getRoutes():
    print(request.args)
    source = request.args.get('source')
    destination = request.args.get('destination')
    source.replace(' ', '+')
    destination.replace(' ', '+')
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+source+'&destination='+destination+'&sensor=false&alternatives=true&mode=driving&key='+key
    r = requests.get(url)
    r = r.text
    d = eval(r)
    d['routes']=d['routes'][0:1]
    return jsonify(d)

@app.route('/findsafety', methods=['POST'])
def findsafety():
    data = request.json
    path = data['routes']
    safety(path)
    return jsonify(data)
def safety(paths):
    print(len(paths))
    factors = ["bakery","bank","beauty_salon","bicycle_store","book_store","cafe","city_hall","clothing_store","convenience_store","courthouse","dentist","department_store","doctor","electronics_store","fire_station","florist","furniture_store","gas_station","home_goods_store","hospital","jewelry_store","library","local_government_office","lodging","movie_theater","pet_store","pharmacy","police","post_office","restaurant","school","shoe_store","shopping_mall","stadium","subway_station","supermarket","synagogue","train_station","transit_station","zoo"]
    index = []
    Places = []
    for route in paths:
        path = route['overview_path']
        index.append([0 for i in range(len(path))])
        for i in range(0,len(path),5):
            lat = path[i]['lat']
            lng = path[i]['lng']
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+str(lng)+"&radius=25&type="
            for factor in factors:
                url += str(factor)+","
            url = url[:-1]
            url += "&key="+key+"&opennow=true"
            r = requests.get(url)
            places = r.json()
            for place in places['results']:
                for factor in place['types']:
                    if factor in factors:
                        index[-1][i] = 1
                        Places.append(place)
    print(len(Places))
    print(index) 
    return 
if __name__ == "__main__":
    app.run(use_reloader=False)
