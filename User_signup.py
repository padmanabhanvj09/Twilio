import json
import random
from sqlwrapper import gensql,dbget

def User_signup(request):
    d = request.json
    print(d)
    if d['user_password'] == d['conf_password']:
       email_count = json.loads(dbget("select count(*) from User_login where \
                                      group_id = '"+d['group_id']+"' and business_id = '"+d['business_id']+"'\
                                      and user_email='"+d['user_email']+"' "))
       if email_count[0]['count'] != 0 :
           return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Email ID Already Exist"},indent=2)) 
       del d['conf_password'] 
       gensql('insert','User_login',d)
       return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
       return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Check Your Password"},indent=2)) 


    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))

def User_login(request):
    d = request.json
    print(d)
    a = { k : v for k,v in d.items() if k not in ('user_password') }
    pw = json.loads(gensql('select','User_login','*',a))
    if pw[0]['user_password'] == d['user_password']: 
       return(json.dumps({"user_name":pw[0]['user_name'],"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
       return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Check Your Password"},indent=2)) 

def Business_signup(request):
    d = request.json
    print(d)
    if d['business_password'] == d['conf_business_password']:
       email_count = json.loads(dbget("select count(*) from business_group where \
                                      group_id = '"+d['group_id']+"' \
                                      and business_email='"+d['business_email']+"' "))
       if email_count[0]['count'] != 0 :
           return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Email ID Already Exist"},indent=2)) 
       del d['conf_business_password']
       conf_no = (random.randint(1000000000,9999999999))
       d['business_id'] = d['business_name'][0:5] + str (conf_no)       
       gensql('insert','business_group',d)
       return(json.dumps({"business_id":d['business_id'],"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
       return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Check Your Password"},indent=2)) 


    return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
