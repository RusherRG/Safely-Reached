from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def test():
    return "Hi"
    
@app.route('/getRoutes', methods=['GET'])
def getRoutes():
    source = request.args.get('source')
    destination = request.args.get('destination')
    source.replace(' ', '+')
    destination.replace(' ', '+')
    key = 'AIzaSyCxb7VjOyG0RqazuliBkyZlP3h437hshkk'
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+source+'&destination='+destination+'&sensor=false&alternativeas=true&mode=driving&key='+key
    r = requests.get(url)
    r = r.text
    return "hello"

app.run(debug=True)