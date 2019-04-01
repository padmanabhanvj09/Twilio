from sqlwrapper import dbget,gensql
import json
import datetime
def updateexistingbooking(request):
     try:
        
        d = request.json
        a = {}
        e = { k : v for k,v in d.items() if k in ('confirmation_number') }
        f = { k : v for k,v in d.items() if v != '' if k not in ('customer_expirydate','confirmation_number','customer_arrival_date','customer_depature_date')}
        print(e,f)
        today_date = datetime.datetime.utcnow().date()
        year = str(today_date.year)
        customer_arrival_date = request.json['customer_arrival_date']
        customer_depature_date = request.json['customer_depature_date']
        if int(customer_arrival_date[0:2]) == today_date.month :
            if int(customer_arrival_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_arrival_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_arrival_date = year+'-'+customer_arrival_date[0:2]+'-'+customer_arrival_date[2:]
        if int(customer_depature_date[0:2]) == today_date.month :
            if int(customer_depature_date[2:]) < today_date.day :
               year = str(today_date.year+1)
               print("year",year,type(year))
        elif int(customer_depature_date[0:2]) < today_date.month :
            year = str(today_date.year+1)
        customer_depature_date = year+'-'+customer_depature_date[0:2]+'-'+customer_depature_date[2:]
        f['customer_depature_date']= customer_depature_date
        f['customer_arrival_date'] = customer_arrival_date
        customer_expirydate = request.json["customer_expirydate"]
        customer_expirydate = customer_expirydate[0:2]+'/'+customer_expirydate[2:]
        f['customer_expirydate'] = customer_expirydate
        a['customer_confirmation_number'] = request.json["confirmation_number"]
        print(gensql('update','ivr_room_customer_booked',f,a))
        
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Success"}))
     except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))

