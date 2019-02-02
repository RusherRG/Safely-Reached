from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__,template_folder=".")

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
    key = 'AIzaSyCxb7VjOyG0RqazuliBkyZlP3h437hshkk'
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+source+'&destination='+destination+'&sensor=false&alternatives=true&mode=driving&key='+key
    r = requests.get(url)
    
    r = r.text
    d = eval(r)
    d['routes']=d['routes'][0:1]
    return jsonify(d)

@app.route('/findsafety', methods=['POST'])
def safety():
    data = request.json
    print(data)
    return jsonify(data)
if __name__ == "__main__":
    app.run(use_reloader=False)
