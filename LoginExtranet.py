import json
from sqlwrapper import gensql,dbfetch

def login(request):

    d = request.json
    email_id = { k : v for k,v in d.items() if k != 'user_password'}
    pw = { k : v for k,v in d.items() if k == 'user_password'}
    print(email_id,pw)
    data = json.loads(gensql('select','extranet_signup','user_password,business_id',email_id))
    data = data[0]
    print(data,type(data))
    if data['user_password'] == pw['user_password']:
       print("password matched")
       
       return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success","Business_id":data['business_id']},indent=2))

    return(json.dumps({"ServiceStatus":"Failure","ServiceMessage":"Failure"},indent=2))
