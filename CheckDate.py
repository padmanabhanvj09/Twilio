import json
import datetime
from sqlwrapper import gensql,dbfetch,dbget


def mobile_no_validation(no):
    if len(no) == 10:
        print(len(no))
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
        print(len(no))
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))
def card_no_validation(cc):
    if len(cc) == 16:
        print(len(cc))
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
        print(len(cc))
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))       
 
def date_validation(date):
    print(date,type(date))
    if len(date) != 8:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"check your date"},indent=2))
    date = date[0:2]+'-'+date[0:2]+'-'+date[4:]
    print(date)
    date = datetime.datetime.strptime(date,'%d-%m-%Y').date()
    print(date,type(date))
    today_date = datetime.datetime.utcnow().date()
    print(today_date)
    if date >= today_date:
       return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"},indent=2))
    else:
       return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))    

def validationivr(request):
    d = request.json
    print(d)
    e = { k : v for k,v in d.items() if v != ''}
    print(e)

    if list(e.keys())[0] == 'date':
        date = e['date']
        print(date,type(date))
        return(date_validation(date))
    elif list(e.keys())[0] == 'mobile':
        no = e['mobile']
        return(mobile_no_validation(no))
    elif list(e.keys())[0] == 'cc':
        cc = e['cc']
        return(card_no_validation(cc))    
