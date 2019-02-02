from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def test():
    return "Hi"
    
@app.route('/getRoutes', methods=['GET'])
def getRoutes():
    print(request.args)
    source = request.args.get('source')
    destination = request.args.get('destination')
    source.replace(' ', '+')
    destination.replace(' ', '+')
    key = 'AIzaSyCxb7VjOyG0RqazuliBkyZlP3h437hshkk'
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+source+'&destination='+destination+'&sensor=false&alternativeas=true&mode=driving&key='+key
    r = requests.get(url)
    r = r.text
    return r
if __name__ == "__main__":
    app.run()