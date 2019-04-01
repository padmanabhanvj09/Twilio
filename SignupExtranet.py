import json
import random
from sqlwrapper import gensql,dbget

def signup(request):
    d = request.json
    #print(d)
    if d['user_password'] == d['user_conf_password']:
       email_count = json.loads(dbget("select count(*) from extranet_signup where hotel_name = '"+d['hotel_name']+"' and user_email = '"+d['user_email']+"' "))
       #print(email_count[0]['count'],type(email_count[0]['count']))
       count = email_count[0]['count']
       if count != 0 :
           return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Email ID Already Exist"},indent=2)) 
       conf_no = (random.randint(1000000000,9999999999))
       conf_no = d['hotel_name'][0:5] + str (conf_no)
       #print(conf_no)
       d['business_id'] = conf_no
       gensql('insert','extranet_signup',d)
       return(json.dumps({"business_id":conf_no,"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
       return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Check Your Password"},indent=2)) 

