from flask import Flask,request

###TESTING

import requests
url = 'http://127.0.0.1:5000/'

###TESTING




def testStr(var):
    if type(var) == type('string'): 
        return True
    else:
        return False

def testInt(var):
    if type(var) == type(1): 
        return True
    else:
        return False
    
    
app = Flask(__name__)

def runWebserver():
    app.run(debug=False)
    #starts web server
    
@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
      					return render_template('../home.html')        
																		#renders the home page
       
    if request.method == 'POST':
        req=request.form
        print("hi")
        postcode=req["Postcode"]
        bedrooms=req["Bedrooms"]
        houseType=req["HouseType"]
        floors=req["Floors"]
        if not testStr(postcode) or not testInt(bedrooms) or not testInt(floors):
            error= "Invalid input"
            print("k")
            return render_template('home.html')        
        else:
            #Find house value
            print("pop")
            

      				
       
        
runWebserver()

### TESTING



###TESTING

