import json
from flask import Flask,request,jsonify
from sqlwrapper import gensql

def queryanitest(request):
    ani = request.args["ani"]
    d,e = {},{}
    d['customer_ani'] = ani
    e['customer_mobile'] = ani
    tab1 = (gensql('select','ivr_customer_profile','customer_language_pref',d))
    print(tab1)
    tab2 = (gensql('select',' ivr_room_customer_booked','*',e))
    print(tab2,type(tab2),len(tab2))
    if len(tab2) == 2:
        return("failure")
    res = json.loads(tab1)
    res = res[0]
    lang = res["customer_language_pref"]
    res1 = json.loads(tab2)
    res1 = res1[0]
    res1['customer_language_pref'] = lang
    #return(json.dumps({"Return":"Record Retrieved Successfully","Return Code":"RRS", "Status": "Success",
     #                 "Status Code": "200", "Return Value":res1},indent=2))
    return("success")
   

    
