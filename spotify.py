#create little flask application using data structures and spotify api
k= "aa1ed5acf98145e7999f1ccff3cc4cd7"
import requests
import pprint as pprint
import json
import time

def api_data(): 
    dummy = []
    response = requests.get(f"https://api.spoonacular.com/food/products/search?query=pizza&maxCalories=500&apiKey=aa1ed5acf98145e7999f1ccff3cc4cd7")
#https://api.spoonacular.com/recipes/complexSearch?apiKey=aa1ed5acf98145e7999f1ccff3cc4cd7
#pprint.pprint(response.json()["products"]) #dict_keys(['type', 'products', 'offset', 'number', 'totalProducts', 'processingTimeMs'])
    for i in response.json()["products"]:
        #print(i["title"])
        dummy.append(i["title"])
       
    return dummy

#print(str(api_data()))
"""with open("temp.txt","w") as f:
    #f.writelines(response.text)
    lines = response.text.split("\n")
    for line in lines:
        f.write(line + "\n")"""


def correct():   
    with open("temp.txt", "r") as f:
        data = f.read()
    # Parse the JSON data
    parsed_data = json.loads(data)
    # Print each line surrounded by curly braces
    for line in json.dumps(parsed_data, indent=4).splitlines():
        time.sleep(2)
        #print("{" + line + "}")

#from spotify import api_data
kev ="+18483134491"
brian = "+19082859375"
me = "+19085252880"
key = "c736ea0feeaa83fb12b0b7bbd137db6ade06c44eyZxELLgX7eCfbun3Stz6QjN2f"
jude = "+19084995282"
malik = "+19088216554"

def sendMSG(message:str):

    key = "c736ea0feeaa83fb12b0b7bbd137db6ade06c44eyZxELLgX7eCfbun3Stz6QjN2f"
    resp = requests.post('https://textbelt.com/text', {
    'phone': "+19085252880",
    'message': str(message),
    'key': key,})
    return resp.json()




def work(mess:str,user:str):
    key = "c7c6b7fae64eced566e58499bd4e1f9d4e828675Eh7B3MMVwc7Noaq3hudS99apJ"
    resp = requests.post('https://textbelt.com/text', {
    'phone': user,
    'message': mess,
    'key': key,
    })
    return resp.status_code , resp.json()
#print(requests.get("google.com"))
#print("me: ", me)
#print("kev: ", kev)
print("started")
#print(work("Hello Brian butler you sex doll that was ordered two weeks ago will arive tonight at 8PM",brian))
print(work("Dear Mr. Malik Wilson, we would like to inform you that the customized sex doll which was ordered under your name two weeks ago, is scheduled to arrive tonight at 8 PM.",malik))
print("done")