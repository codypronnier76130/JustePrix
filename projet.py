from flask import Flask, render_template, request
import requests, json
import random
import datetime
import time

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():

  nombreDeBase = random.randint(1,20)
  
  price = -1
  historique = []
  firsttrytime = -1 
  if request.method == "POST": 
    nombreDeBase = int(request.form["nombredebase"])
    price = int(request.form["champprix"])
    historique = json.loads(request.form["historique"])
    historique.append(price)
    firsttrytime = float(request.form["firsttrytime"])
    if firsttrytime == -1 :
       firsttrytime = time.time()

  params = {
            "ApiKey": "818e864c-7f59-41db-8546-6498f3d90ef0",
            "SearchRequest": {
              "Keyword": "ecran",
              "Pagination": {
                "ItemsPerPage": nombreDeBase,
                "PageNumber": 1
              },
              "Filters": {
                "Price": {
                  "Min": 0,
                  "Max": 0
                },
                "Navigation": "",
                "IncludeMarketPlace": "false"
              }
            }
          }
      
    

  url = "https://api.cdiscount.com/OpenApi/json/Search"
 
  r = requests.post(url, data=json.dumps(params))
  nom =(r.json()['Products'][0]['Name'])
  prix = int(float(r.json()['Products'][0]['BestOffer']['SalePrice']))
  image =(r.json()['Products'][0]['MainImageUrl'])

  tempstotal = None
  if request.method == "POST": 
    tempstotal = datetime.datetime.now() - datetime.datetime.fromtimestamp(firsttrytime)

  return render_template("hello.html", NOM=nom, PRIX=prix, IMAGE=image, PRICE=price, NOMBREDEBASE=nombreDeBase, HISTORIQUE=historique, FIRSTTRYTIME=firsttrytime, TEMPSTOTAL=tempstotal)

if __name__ == "__main__":
    app.run()