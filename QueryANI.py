import json
from flask import Flask,request,jsonify
from sqlwrapper import gensql

def queryani(request):
  try:
    ani = request.args["ani"]
    d,e = {},{}
    d['customer_ani'] = ani
    e['customer_mobile'] = ani
    tab1 = (gensql('select','ivr_customer_profile','customer_language_pref',d))
    print(tab1)
    tab2 = (gensql('select',' ivr_room_customer_booked','*',e))
    print(tab2,type(tab2))
    res = json.loads(tab1)
    res = res[0]
    lang = res["customer_language_pref"]
    res1 = json.loads(tab2)
    res1 = res1[0]
    res1['customer_language_pref'] = lang
    print(res1,type(res1))
    dict1 = {"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                      "Status_Code": "200"}
    print(dict1,type(dict1))
    dict1.update(res1)
    print(dict1)
    return(json.dumps(dict1))
  except:
    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))

    
