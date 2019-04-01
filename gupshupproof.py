from sqlwrapper import gensql,dbget,dbput
import json
#import re
from flask import Flask,request,jsonify
def updategupshupreservation(request):
    try:
        if request.method == 'GET':
            customer_mobile = request.args['customer_mobile']
            id_proof = request.args['id_proof']
        if request.method == 'POST':
            customer_mobile = request.json['customer_mobile']
            id_proof = request.json['id_proof']
        
        dbput("update  ivr_room_customer_booked set id_proof='"+str(id_proof)+"' where customer_mobile='"+(customer_mobile)+"'")
        print("mohan")
        return(json.dumps({"Message":"Record Updated Successfully","Message_Code":"RUS","Service_Status":"Success","id_proof":id_proof},indent=4))
        
    except:
        return(json.dumps({"Message":"Recored Updated UnSuccessfully","Message_Code":"RUUS","Service":"Failure"},indent=4))
