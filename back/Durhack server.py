from flask import Flask, request,render_template, redirect, url_for


def testStr(var): #Test for or string
    if type(var) == type('string'):
        return True
    else:
        return False

def testPostLen(var):
    if len(var) in [6, 7]:
        return True
    else:
        return False

def testInt(var): #Tests if integer entered
    try:
        int(var)
        return True
    except:
        return False

def testNull(var): #Tests for blank input
    if var != "":
        return True
    else:
        return False


app = Flask(__name__)


def runWebserver():
    app.run(debug=True)
    # starts web server


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    # renders the home page

    if request.method == 'POST':
        req = request.form
        postcode = req["Postcode"] #Recieves each variable from site
        bedrooms = req["Bedrooms"]
        houseType = req["HouseType"]
        garden = req["Garden"]

        if garden == "yes": #Convert garden to boolean
            garden == True
        elif garden == "no":
            garden == False

        if not testStr(postcode) or not testInt(bedrooms) or not testNull(garden) or not testNull(houseType) or not testPostLen(postcode) :
            error = "Invalid input"
            return render_template('home.html',error=error) #Reloads page with error bein invalid input

        else:
            bedrooms = int(bedrooms)
            # Find house value
            # price = calculations(postcode,bedrooms,houseType,Garden)
            price = 1
            return redirect(url_for("result", price = price)) #Sends value of house to 2nd page

@app.route("/result", methods=['GET', 'POST'])
def result():
    price = request.args.get('price') #retrieves price value
    return render_template('render.html',price=price) #renders page with variable price in web code being set to price


runWebserver()

