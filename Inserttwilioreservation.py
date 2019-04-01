from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from collections import Counter
import random
import urllib
from dateutil import parser
from decimal import Decimal
import math
import matplotlib.pyplot as plt
def Inserttwilioreservation(request):
    if request.method == 'GET':
        d = {}
        no_room = request.args['customer_no_of_rooms']
        roomtype = request.args['customer_room_type']
        arr = request.args['customer_arrival_date']
        dep = request.args['customer_depature_date']
        tfn = '+'+request.args['TFN']
        cntry_code = request.args['cntry_code']
        d['channel'] = request.args['channel']
        d['customer_booked_status'] = request.args['customer_booked_status']
        d['modification'] = request.args['modification']
        d['ivr_language'] = request.args['ivr_language']
        d['rate_per_day'] = request.args['rate_per_day']
        d['customer_adult'] = request.args['customer_adult']
        d['customer_child'] = request.args['customer_child']
        d['customer_name'] = request.args['customer_name']
        d['customer_email'] = request.args['customer_email']
        d['customer_mobile'] = request.args['customer_mobile']
        d['customer_pickup_drop'] = request.args['customer_pickup_drop']
        d['customer_amount'] = request.args['customer_amount']
        d['nights'] = request.args['nights']
        print("abc",d['rate_per_day'])
        list1 = d['rate_per_day'].replace("total",'amount')
        list1 = list1.replace("day",'rate_date')
        #list1 = list1.replace(",",'''",''')
        list1 = list1.replace('}"',"}")
        list1 = list1.replace('}{','},{')
        list1 = '['+list1+']'
        print(list1,type(list1))
        rate_per_day = json.loads(list1)
        
    if request.method == 'POST':
        d = request.json
        tfn = request.json['TFN']
        no_room = request.json['customer_no_of_rooms']
        roomtype = request.json['customer_room_type']
        arr = request.json['customer_arrival_date']
        dep = request.json['customer_depature_date']
        roomtype = request.json['customer_room_type']
        cntry_code = request.json['cntry_code']
    #print("rate_per_day",d['rate_per_day'][1:-1],type(d['rate_per_day']))
        list1 = d['rate_per_day'].replace("total=",'"amount":')
        list1 = list1.replace("day=",'''"rate_date":"''')
        list1 = list1.replace(",",'''",''')
        list1 = list1.replace('}"',"}")
        list1 = list1.replace('}{','},{')
        list1 = '['+list1+']'
        print(list1,type(list1))
        rate_per_day = json.loads(list1)
    
    #print("rate_per_day",rate_per_day,type(rate_per_day))

    
    d= {k:v for k,v in d.items() if k not in ('TFN','rate_per_day')}
    #tfn = request.json['TFN']

    
    if cntry_code.find('+') != -1:
        pass
    else:
        cntry_code = '+'+cntry_code
    print("cntry_code", cntry_code)
    
    b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
    #print(b_id)
    bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
    print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
    
    
    
    customer_arrival_date = parser.parse(arr).date().strftime('%Y-%m-%d')
    customer_depature_date = parser.parse(dep).date().strftime('%Y-%m-%d')
    customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
    customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

    today_date = datetime.datetime.utcnow().date()
    if customer_arrival_date < today_date:
            customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
    if customer_depature_date < today_date:
            customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
    #print("arr",customer_arrival_date)
    #print("dep",customer_depature_date)
    
    confir = (random.randint(100000,999999))
    
    d['customer_arrival_date'] = customer_arrival_date
    d['customer_depature_date'] = customer_depature_date
    d['customer_confirmation_number'] = confir
    d['modification'] = "No"
    d['customer_booked_status'] = d['customer_booked_status'].lower()
    d['customer_room_type'] = roomtype.title()
    d['business_id'] = str(bi_id[0]['business_id'])
    d['booked_date'] = today_date = datetime.datetime.utcnow()
    d['cntry_code'] = cntry_code
    
    sql = gensql('insert','public.ivr_room_customer_booked',d)
    print(sql)
    
    for rate in rate_per_day:
        print(rate)
        rate['customer_confirmation_number'] = confir
        rate['business_id'] = str(bi_id[0]['business_id'])
        gensql('insert','customer_rate_detail',rate)
    psql = json.loads(dbget("select room_id from configration where room_name = '"+str(d['customer_room_type'])+"'"))
    print(psql)
    depature_date1 = customer_depature_date-datetime.timedelta(days=1)
    print(depature_date1)
    
    dbput("update room_to_sell set available_count=available_count-"+str(no_room)+", booked_count=booked_count+"+str(no_room)+" where\
         business_id='"+str(bi_id[0]['business_id'])+"' and room_id='"+str(psql[0]['room_id'])+"'\
         and room_date between '"+str(customer_arrival_date)+"' and '"+str(depature_date1)+"' ")
    
    return(json.dumps([{"Return":"Record Inserted Succcessfully","Returncode":"RIS",
                        "Status":"Success","Statuscode":200,"confirmation_number":confir,
                        "business_id":bi_id[0]['business_id']}],indent=2))
       
def InsertArrivalDeparture(request):
    if request.method == 'GET':
        d = {}
        data1 = request.args['customer_arrival_date']
        data2 = request.args['customer_depature_date']
        print(data1,data2)
    if request.method == 'POST':
        d = request.json
        print(d)
        data1 = d.get('customer_arrival_date')
        data2 = d.get('customer_depature_date')
    try:
        #e = { k : v for k,v in d.items() if v = '' }       
        #print(e)
        today_date = datetime.datetime.utcnow().date()
        print(today_date)
        '''
        arrival = e['arrival']
        depature = e['departure']
        print(arrival,depature,type(arrival))
        arr_date = datetime.datetime.strptime(arrival, '%Y-%m-%d').date()
        dep_date = datetime.datetime.strptime(depature, '%Y-%m-%d').date()
        print("str1", arr_date,dep_date,type(arr_date))
        '''
        #data1 = d.get('customer_arrival_date')
        #data2 = d.get('customer_depature_date')
        date1 = parser.parse(data1).date().strftime('%d-%m-%Y')
        date2 = parser.parse(data2).date().strftime('%d-%m-%Y')    
        arr_date = datetime.datetime.strptime(date1, '%d-%m-%Y').date()     #datetime format
        dep_date = datetime.datetime.strptime(date2, '%d-%m-%Y').date()
        arr_date = arr_date.strftime("%Y-%m-%d")                             #formatted string datetime
        dep_date = dep_date.strftime("%Y-%m-%d")
        arr_date = datetime.datetime.strptime(arr_date, '%Y-%m-%d').date()   #convert string to datetime format
        dep_date = datetime.datetime.strptime(dep_date, '%Y-%m-%d').date()
        print(arr_date,dep_date)
        
        today_date = datetime.datetime.utcnow().date()
        if arr_date < today_date:
            arr_date = arr_date+datetime.timedelta(days=365)
        if dep_date < today_date:
            dep_date = dep_date+datetime.timedelta(days=365)
            
        restrict_days =  today_date + datetime.timedelta(days=90)
        print(restrict_days)
        #charges_end_date = datetime.datetime.strptime(data2, '%Y-%m-%d').date()
        #print("str2",charges_begin_date,charges_end_date,type(charges_end_date))
        d['arrival'] = arr_date
        d['departure'] = dep_date
        if arr_date >= today_date:
            if  dep_date >= arr_date :    
                if dep_date <= restrict_days:
                   #sql_value = gensql('insert','reservation',d)
                   return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Given dates are valid','ReturnCode':'Valid'}], sort_keys=True, indent=4))
                else:   
                   return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'departure date should not exceed 90 days than arrival','ReturnCode':'Invalid'}], sort_keys=True, indent=4))
            else:
                
               return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Departure date should not be in past date than arrival','ReturnCode':'Invalid'}], sort_keys=True, indent=4))
        else:
            
             return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'arrival date must be scheduled atleast one day in advance','ReturnCode':'Invalid'}], sort_keys=True, indent=4))
    except:
         return(json.dumps([{'Status': 'Success', 'StatusCode': '200','ReturnCode':'Invalid'}], sort_keys=True, indent=4))

        

def Modifytwilioreservation(request):
    if request.method == 'GET':
        d= {}
        tfn=request.args['TFN']
        d['customer_confirmation_number']=request.args['customer_confirmation_number']
        d['customer_arrival_date']=request.args['customer_arrival_date']
        d['customer_depature_date']=request.args['customer_depature_date']
        d['rate_per_day']=request.args['rate_per_day']
        d['customer_name']=request.args['customer_name']
        d['customer_email']=request.args['customer_email']
        d['customer_adult']=request.args['customer_adult']
        d['customer_child']=request.args['customer_child']
        d['customer_room_type']=request.args['customer_room_type']
        d['customer_mobile']=request.args['customer_mobile']
        d['cntry_code']=request.args['cntry_code']
        d['channel']=request.args['channel']
        d['customer_pickup_drop']=request.args['customer_pickup_drop']
        d['customer_no_of_rooms']=request.args['customer_no_of_rooms']
        d['customer_amount']=request.args['customer_amount']
        d['modification']=request.args['modification']
        d['customer_booked_status']=request.args['customer_booked_status']
        d['nights']=request.args['nights']
        d['ivr_language']=request.args['ivr_language']
    if request.method == 'POST':
        d = request.json
        tfn = request.json['TFN']
    #print(d)
    
    a = { k : v for k,v in d.items() if v != '' if k not in ('customer_confirmation_number',
                                                             'customer_arrival_date','customer_depature_date',
                                                             'rate_per_day','TFN')}
    #print(a)
    
    
    b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
    #print(b_id)
    bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
    print(bi_id[0]['business_id'],type(bi_id[0]['business_id'])) 
    #print(a)
    e = { k : v for k,v in d.items()  if k in ('customer_confirmation_number')}
    #print(e)

    get = json.loads(gensql('select','ivr_room_customer_booked','*',e))

    #print("get",get)
    
    if len(get) == 0:
        return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Invalid Confirmation Number',
                        'ReturnCode':'ICN'}], sort_keys=True, indent=4)) 
    if get[0]['customer_booked_status'] in ('canceled'):
        return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Can Not Modify This Reservation',
                        'ReturnCode':'CNM'}], sort_keys=True, indent=4)) 
                          
    list1 = d['rate_per_day'].replace("total=",'"amount":')
    list1 = list1.replace("day=",'''"rate_date":"''')
    list1 = list1.replace(",",'''",''')
    list1 = list1.replace('}"',"}")    
    rate_per_day = json.loads(list1)

    cntry_code = request.json['cntry_code']
    if cntry_code.find('+') != -1:
        pass
    else:
        cntry_code = '+'+cntry_code
    print("cntry_code", cntry_code)
    
    customer_arrival_date = d['customer_arrival_date']
    customer_depature_date = d['customer_depature_date']
    
    customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
    customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
    customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
    customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

    today_date = datetime.datetime.utcnow().date()
    if customer_arrival_date < today_date:
        customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
    if customer_depature_date < today_date:
        customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
    #print("arr",customer_arrival_date)
    #print("dep",customer_depature_date)
    
    a['customer_arrival_date'] = customer_arrival_date
    a['customer_depature_date'] = customer_depature_date
    a['booked_date'] = today_date = datetime.datetime.utcnow()
    a['cntry_code'] = cntry_code

    
    depature_date1 = datetime.datetime.strptime(get[0]['customer_depature_date'], '%Y-%m-%d').date()-datetime.timedelta(days=1)
    
    r_id = json.loads(dbget("select room_id from configration where room_name = '"+str(get[0]['customer_room_type'])+"'"))
    print("r",r_id)
    
    dbput("update room_to_sell set available_count=available_count+'"+str(get[0]['customer_no_of_rooms'])+"',\
          booked_count=booked_count-'"+str(get[0]['customer_no_of_rooms'])+"' where\
          business_id='"+str(get[0]['business_id'])+"' and \
          room_id='"+str(r_id[0]['room_id'])+"' \
          and room_date between \
          '"+str(get[0]['customer_arrival_date'])+"' and '"+str(depature_date1)+"' ")
    
    
    sql_value = gensql('update','ivr_room_customer_booked',a,e)
    #print(sql_value)
    
    dbput("delete from customer_rate_detail where customer_confirmation_number='"+str(e['customer_confirmation_number'])+"'\
           and business_id='"+str(bi_id[0]['business_id'])+"' ")

    for rate in rate_per_day:
        #print(rate)
        rate['customer_confirmation_number'] = e['customer_confirmation_number']
        rate['business_id'] = str(bi_id[0]['business_id'])
        gensql('insert','customer_rate_detail',rate)
        
    depature_date1 = customer_depature_date-datetime.timedelta(days=1)
    r_id = json.loads(dbget("select room_id from configration where room_name = \
                            '"+str(a['customer_room_type'])+"'"))
    print("r",r_id)
    
    dbput("update room_to_sell set available_count=available_count-"+a['customer_no_of_rooms']+",\
           booked_count=booked_count+"+a['customer_no_of_rooms']+" where\
           business_id='"+str(bi_id[0]['business_id'])+"' and room_id='"+str(r_id[0]['room_id'])+"'\
           and room_date between '"+str(a['customer_arrival_date'])+"' and '"+str(depature_date1)+"' ")
    

    return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Record Updated Successfully',
                        'ReturnCode':'RUS',"confirmation_number":e['customer_confirmation_number'],
                        "business_id":bi_id[0]['business_id']}], sort_keys=True, indent=4))

def Canceltwilioreservation(request):
    if request.method == 'GET':
        conf = request.args['confirmation_number']
    if request.method == 'POST':
        conf = request.json['confirmation_number']
    d = {}
    #conf = request.json['confirmation_number']
    d['customer_confirmation_number'] = conf
    
    res = json.loads(gensql('select','ivr_room_customer_booked','*',d))
    
    if len(res) == 0 :
        return(json.dumps([{"Return":"Invalid Confirmation Number","Return_Code":"ICN","Status": "Success",
                      "Status_Code": "200"}],indent=2))
    
    if res[0]['customer_booked_status'] in ('canceled','not booked'):
        return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Can Not Modify This Reservation',
                        'ReturnCode':'CNM'}], sort_keys=True, indent=4)) 

     
    result  = json.loads(res)
    data = result[0]
    date = data['customer_arrival_date']
    date1 = data['customer_depature_date']
    arrival_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    depature_date = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    str_date = "'"+str(arrival_date)+"'"
    while arrival_date < depature_date:
          arrival_date = arrival_date+datetime.timedelta(days=1)
          str_date += ","+"'"+str(arrival_date)+"'"
    #print(str_date)    
    room_type = data['customer_room_type']
    #print(room_type)
    no_of_room = data['customer_no_of_rooms']
    b_id = data['id']
    #print(no_of_room,b_id)
    
    today_date = datetime.datetime.utcnow().date()
    if arrival_date < today_date:
       return(json.dumps([{"Return":"Can't Cancel Reservation","Return_Code":"CCR","Status": "Success",
                      "Status_Code": "200"}],indent=2))
    s = {}
    s['customer_booked_status'] = "canceled"    
    gensql('update','ivr_room_customer_booked',s,d)
    bu_id = json.loads(dbget("select business_id,customer_no_of_rooms,customer_arrival_date,customer_room_type,customer_depature_date from ivr_room_customer_booked where customer_confirmation_number = '"+str(conf)+"' "))
    #print(bu_id[0]['business_id'])
    arr = str(bu_id[0]['customer_arrival_date'])
    end = str(bu_id[0]['customer_depature_date'])
    print(bu_id[0]['customer_arrival_date'])
    rm_name = bu_id[0]['customer_room_type']
    #print(arr,type(arr),rm_name)
    psql = json.loads(dbget("select room_id from configration where room_name = '"+str(rm_name)+"'"))
    #print(psql)
    dbput("update room_to_sell set available_count=available_count+'"+str(bu_id[0]['customer_no_of_rooms'])+"',\
          booked_count=booked_count-'"+str(bu_id[0]['customer_no_of_rooms'])+"' where\
          business_id='"+str(bu_id[0]['business_id'])+"' and room_id='"+str(psql[0]['room_id'])+"' and room_date between '"+str(arr)+"' and '"+str(end)+"' ")
    
    return(json.dumps([{'Status': 'Success', 'StatusCode': '200','Return': 'Your booking has been cancelled',
                        'ReturnCode':'RCS'}], sort_keys=True, indent=4))

def Smstwilioservice(request):
    if request.method == 'GET':
        countrycode = request.args['countrycode']
        print("countrycode", countrycode)
        #print(countrycode)
        name = 'Customer'
        phone = request.args['phone']
        message = request.args['message']
        conf_no = request.args['conf_no']
        hotel_name = 'Konnect'
        arrival = request.args['arrival']
        depature = request.args['depature']
        room_type = request.args['room_type']
    if request.method == 'POST':
        countrycode = request.json['countrycode']
        print("countrycode", countrycode)
        #print(countrycode)
        name = 'Customer'
        phone = request.json['phone']
        message = request.json['message']
        conf_no = request.json['conf_no']
        hotel_name = 'Konnect'
        arrival = request.json['arrival']
        depature = request.json['depature']
        room_type = request.json['room_type']

    if countrycode.find('+') != -1:
        pass
    else:
        countrycode = '+'+countrycode
    all_message = ("Dear "+name+", "+message+".  Confirmation Number is "+conf_no+", Arrival Date: "+arrival+", Depature Date:"+depature+", Room Type:"+room_type+". by "+hotel_name+"")
    url = "https://control.msg91.com/api/sendhttp.php?authkey=195833ANU0xiap5a708d1f&mobiles="+phone+"&message="+all_message+"&sender=Infoit&route=4&country="+countrycode+""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        the_page = the_page[1:]
        print(the_page)
        the_page = str(the_page)
    sql = dbput("update ivr_room_customer_booked set send_sms = 'success' where customer_confirmation_number = '"+conf_no+"'")
    print(sql)
    return(json.dumps([{"Return":"SMS Sent Successfully","Return_Code":"SSS","Status": "Success","Status_Code": "200","Key":the_page}],indent =2))

def CheckConfirmation(request):
    if request.method == 'GET':
        conf_no = request.args['confirmation_number']
        
    if request.method == 'POST':
         conf_no = request.json['confirmation_number']
     
    #sql = json.loads(dbget("select count(*) from ivr_room_customer_booked where customer_confirmation_number='"+conf_no+"'"))
    psql = json.loads(dbget("select count(*) from ivr_room_customer_booked where customer_confirmation_number='"+conf_no+"' and customer_booked_status in ('booked')"))
    print(psql)
    if  psql[0]['count'] != 0 :
         return(json.dumps([{"Return":"Confirmation number already exist","Return_Code":"Valid","Status": "Success","Status_Code": "200"}],indent =2))
    else:
         return(json.dumps([{"Return":"Confirmation number does not exist","Return_Code":"Invalid","Status": "Success","Status_Code": "200"}],indent =2))
        
        
def twiliofetchroomsavailabilityandprice(request):
    #try:
        if request.method == 'GET':
            d={}
            tfn = '+'+request.args['TFN']
            d['adult']=request.args['adult']
            d['child']=request.args['child']
            d['arrival_date']= request.args['arrival_date']
            d['depature_date']=request.args['depature_date']
        if request.method == 'POST':    
            d = request.json
            print(d)
            tfn = request.json['TFN']
        adult = d['adult']
        child = d['child']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        #print(b_id)#,b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        #print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        #d['customer_arrival_date'] = datetime.date(2019, 1, 1)
        #d['customer_depature_date'] = datetime.date(2019, 1, 3)
        customer_arrival_date = d['arrival_date']
        customer_depature_date = d['depature_date']
        customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
        customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
        customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
        customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()
        today_date = datetime.datetime.utcnow().date()
        if customer_arrival_date < today_date:
            #year = customer_arrival_date.year
            #print("year",year,type(year))
            customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
        if customer_depature_date < today_date:
            customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
        
        
        nights = customer_depature_date.day - customer_arrival_date.day
        
        #print("nights",customer_arrival_date,type(customer_arrival_date))

        depature_date1 = customer_depature_date-datetime.timedelta(days=1)

        #print("depature_date1",depature_date1)

        
        room_to_sell = json.loads(dbget("select * from room_to_sell where room_date between '"+str(customer_arrival_date)+"'\
                                         and '"+str(depature_date1)+"' and business_id='"+bi_id[0]['business_id']+"' "))
        
        #print("room_to_sell",room_to_sell,type(room_to_sell))
        
        count_o, count_l = [],[]
        
        for i in room_to_sell:
              if i['available_count'] == 0 or i['available_count'] == None:
                      count_o.append(i['room_id'])           
              else:
                 if i['room_id'] not in count_l:
                    count_l.append(i['room_id'])
        #print(count_o, count_l)

        for i in  count_o:
            count_l = [x for x in count_l if x != i]

        count_ll = list(map(str, count_l))        
        #print("idssss   ",count_l,count_ll)    
        if len(count_l) == 0:
              return(json.dumps([{"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                              "Status_Code": "200","total":{"count":0}}],indent=2))      
        rates = json.loads(dbget("select extranet_availableroom.room_id, configration.room_name, room_date,\
                                  room_rate,extranet_availableroom.extra_adult_rate,\
                                  room_open, extranet_availableroom.rate_plan_id from extranet_availableroom \
                                  join configration on extranet_availableroom.room_id = configration.room_id where\
                                  room_date between \
                                  '"+str(customer_arrival_date)+"' and '"+str(depature_date1)+"' and \
                                  extranet_availableroom.business_id = '"+bi_id[0]['business_id']+"' and \
                                  extranet_availableroom.room_id in (%s) order by room_id asc, room_date asc" % ",".join(map(str,count_ll))))
        #print(rates)

        beds = json.loads(dbget("select configration.room_id,configration.room_name, bedding_options.total_bed , max_extra_bed.extrabed from configration join \
                                 bedding_options on configration.bedding_options_id = bedding_options.bedding_option_id\
                                 join max_extra_bed on configration.maximum_extrabed_id = max_extra_bed.extrabed_id \
                                 where  configration.business_id='"+bi_id[0]['business_id']+"' and \
                                 configration.room_id in (%s)" % ",".join(map(str,count_ll))))
        #print("beds",beds)
        #print("adult",adult)
        plans, total =[],[]
        list1 =[]
        
        for room_id in count_l:
            list1 = []
            #plan_ids = []
            plans = []
            for rate in rates:
                if rate['room_id'] == room_id:                       
                       #print(rate,rates.index(rate))
                       r = {}
                       r['room_id'] = rate['room_id']
                       r['roo_name'] = rate['room_name']
                       r['rate_plan_id'] = rate['rate_plan_id']
                       r['room_date'] = rate['room_date']
                       r['room_rate'] = rate['room_rate']
                       r['extra_adult_rate'] = rate['extra_adult_rate']
                       plans.append(r)
            #print("plans",plans)
            plan_ids = []
            for plan in plans:
                
                if plan['room_date'] in plan_ids:
                   #print(len(list1),"len list....if")     
                   list1[len(list1)-1].append(plan)
                   
                else:
                   plan_ids.append(plan['room_date'])
                   list1.append([])
                   #print(len(list1),"len list....else")
                   list1[len(list1)-1].append(plan)
                
                
            #print("plans, list1",plan_ids, list1)

            r1 = {}
            r1['room_id'] = room_id
            r1['rate_plans'] = list1
            total.append(r1)
        add_amount,final = [], []
        amount = {}
        count = 0
        for bed in beds:    
            for tol in total:
                if tol['room_id'] == bed['room_id'] and len(tol['rate_plans']) != 0:    
                   total_bed = bed['total_bed']
                   extrabed = bed['extrabed']
                   #print("total_bed: ", total_bed,"and ", "extrabed: ", extrabed )
                   rate_plan = tol['rate_plans']
                   extra_adult = int(adult) - int(total_bed)
                   for plan in rate_plan:
                        room_rate, extra_adult_rate =[],[] 
                        for p in plan:
                            room_rate.append(p['room_rate'])
                            extra_adult_rate.append(p['extra_adult_rate'])
                        #print("extra_adult_rate", extra_adult_rate, type(extra_adult_rate))    
                        if extra_adult != 0 and extra_adult > 0:
                           r1 = float(room_rate[0] + extra_adult_rate[0]*extra_adult)
                        else:
                           r1 = room_rate[0] 
                        #print("r1",r1,type(r1))
                        add_amount.append(r1)
                        #print("add_amount", add_amount,type(add_amount))
                   amount['amount'+""+str(count)+""] = sum(add_amount)     
                   amount['room_id'+""+str(count)+""] = bed['room_id']
                   amount['room_name'+""+str(count)+""] = bed['room_name']
                   print("amount", amount)
                   count += 1
                   add_amount = []
            final.append(amount)
    
        #print(total)
        #print(add_amount)
        amount['count'] = count
        #print("final",final,amount)
        return(json.dumps([{"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                              "Status_Code": "200","total":amount}],indent=2))  
    
def twiliocalculatetotalcharges(request):
    #try:
        if request.method == 'GET':
            tfn = '+'+request.args['tfn_num']
            customer_arrival_date = request.args["arrival_date"]
            customer_depature_date = request.args["depature_date"]
            customer_room_type = request.args["room_type"] # ROOM_ID
            customer_adult = request.args["adult"]
            customer_child = request.args["child"]
        if request.method == 'POST':
            tfn = request.json['tfn_num']
            customer_arrival_date = request.json["arrival_date"]
            customer_depature_date = request.json["depature_date"]
            customer_room_type = request.json["room_type"] # ROOM_ID
            customer_adult = request.json["adult"]
            customer_child = request.json["child"]
        dividen_list = []
        last_list = []
        sumval = 0
        datelist_rate = []
        datelist_amount = {}
        rate_plan_list = []
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        
        #print(customer_room_type,type(customer_room_type))
        roos_type_id = json.loads(dbget("select room_id from configration where room_name = '"+str(customer_room_type.title())+"'"))
       # customer_room_type = customer_room_type.title()
       # print("roomtype",customer_room_type)
        print("adults",customer_adult,type(customer_adult))
        d,e,d1,d2 = {},[],{},{}
        
        customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
        customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
        customer_arrival_date = datetime.datetime.strptime(customer_arrival_date,'%Y-%m-%d').date()
        customer_depature_date = datetime.datetime.strptime(customer_depature_date,'%Y-%m-%d').date()

        today_date = datetime.datetime.utcnow().date()
        if customer_arrival_date < today_date:
            customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
        if customer_depature_date < today_date:
            customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
        print("arr",customer_arrival_date)
        print("dep",customer_depature_date)
        
        number_of_nights = customer_depature_date.day - customer_arrival_date.day
        print(number_of_nights)
        customer_depature_date -= datetime.timedelta(days=1)
        sql = json.loads(dbget("select max_extra_bed.extrabed,extranet_availableroom.extra_adult_rate,extranet_availableroom.rate_plan_id,extranet_availableroom.room_date,extranet_availableroom.room_rate,configration.max_adults \
                                    from configration \
                                   join extranet_availableroom on extranet_availableroom.room_id = configration.room_id \
                                   join max_extra_bed on max_extra_bed.extrabed_id = configration.maximum_extrabed_id \
                                   where configration.room_id  = '"+str(roos_type_id[0]['room_id'])+"' and configration.business_id='"+bi_id[0]['business_id']+"'and extranet_availableroom.room_date between '"+str(customer_arrival_date)+"' and '"+str(customer_depature_date)+"' order by room_date"))
        print("sql",len(sql))
     
            
        plan_id_list = [v for s in sql for k,v in s.items()  if k == 'rate_plan_id' ]
        print("ok d",plan_id_list)
        
        my_dict = [k for k,v in dict(Counter(plan_id_list)).items() if v == number_of_nights]

        print(my_dict)

        sql = [ s  for s in sql   if s['rate_plan_id'] in my_dict ]
        print("sql",len(sql))
        
        if len(sql) == 0:
            
            return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))

        plan_id = sql[0]['rate_plan_id']
        #print("plan_id",plan_id)
        s = 0
        total_adult = int(customer_adult)
        max_adult = int(sql[0]['max_adults'])
        extra_bed = int(sql[0]['extrabed'])
        extra_adult_rate = sql[0]['extra_adult_rate']
        rooms_rate =  int(sql[0]['room_rate'])
        
        plan_rate = int(sql[0]['rate_plan_id'])

        #print("plan_rate",plan_rate)
        total_beds = max_adult + extra_bed
        total_rooms = total_adult / total_beds
        total_rooms_count = math.ceil(total_rooms)
        print("no of rooms",total_rooms_count)
        
    
        sumva = 0
        arrival_date = customer_arrival_date
        depature_date = customer_depature_date

        for i in sql:
            
            if i['rate_plan_id'] == plan_id:
                
                #print(i['room_date'],type(i['room_date']))
                r1 = max_adult * total_rooms_count
                extra_price = (int(customer_adult) - r1) * int(i["extra_adult_rate"])
                price = total_rooms_count * int(i['room_rate'])
                total = price + extra_price
                add_date = datetime.datetime.strptime(i['room_date'],'%Y-%m-%d').date()+ datetime.timedelta(days=1)
                
                datelist_rate.append({"day":""+datetime.datetime.strptime(i['room_date'],'%Y-%m-%d').date().strftime("%d")+""+
                                      " "+datetime.datetime.strptime(i['room_date'],'%Y-%m-%d').date().strftime("%B")[:3]+""+" - "+
                                       ""+add_date.strftime("%d")+""+" "+""+add_date.strftime("%B")[:3]+"",
                                      "total":total})
                      
        
        
        
        def myconverter(o):
                    if isinstance(o, datetime.datetime):
                         return o.__str__()  
 
        return(json.dumps([{"ServiceMessage":"Success","Total_Amount":total*number_of_nights,"date_amount":datelist_rate,
                            "no_of_rooms":total_rooms_count,"number_of_nights":number_of_nights}],indent=2,default=myconverter))
        
        #return(json.dumps({"ServiceMessage":"Success","Total_Amount":total_amout,"date_month_amount":last_list},indent=2))
        
    #except:
       # return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))

def CheckRoomtype(request):
    if request.method == 'GET':
        tfn = '+'+request.args['TFN']
        d={}
        d['customer_arrival_date']= request.args['customer_arrival_date']
        d['customer_depature_date']=request.args['customer_depature_date']
        d['customer_room_type'] = request.args['customer_room_type']
    if request.method == 'POST':
        d = request.json
        print(d)
        tfn = d['TFN']
    customer_arrival_date = d['customer_arrival_date']
    customer_depature_date = d['customer_depature_date']
    #d = {k:v for k,v in d.items() if k not in ('TFN')}
    b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
    print(b_id)#,b_id[0]['id'])
    bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
    print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))

    customer_room_type = d['customer_room_type']
    
    customer_room_type = customer_room_type.title()
    
    sql = json.loads(dbget("select count(*) from configration where room_name = '"+str(customer_room_type)+"'"))
    print(sql,sql[0]['count'],type(sql[0]['count']))

    if sql[0]['count'] == 0:
        
        return(json.dumps([{'Retuen':'Success','Returncode':'InValid'}]))
    
    room_type_id = json.loads(dbget("select room_id from configration where room_name = '"+str(customer_room_type)+"'"))

    print(room_type_id[0]['room_id'],type(room_type_id[0]['room_id']))

    customer_arrival_date = parser.parse(customer_arrival_date).date().strftime('%Y-%m-%d')
    customer_depature_date = parser.parse(customer_depature_date).date().strftime('%Y-%m-%d')
    customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
    customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

    today_date = datetime.datetime.utcnow().date()
    if customer_arrival_date < today_date:
        customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
    if customer_depature_date < today_date:
        customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
            
    print("arr",customer_arrival_date)
    print("dep",customer_depature_date)
    
    nights = customer_depature_date.day - customer_arrival_date.day
        
    print("nights",nights,type(nights))

    depature_date1 = customer_depature_date-datetime.timedelta(days=1)

    print("depature_date1",depature_date1)

        
    count = json.loads(dbget("select count(*) from room_to_sell where room_id='"+str(room_type_id[0]['room_id'])+"' and \
                              room_date between '"+str(customer_arrival_date)+"' \
                              and '"+str(depature_date1)+"' and business_id='"+bi_id[0]['business_id']+"' "))

    print("count",count[0]['count'],type(count[0]['count']))


    if int(count[0]['count']) == int(nights):
        return(json.dumps([{'Retuen':'Success','Returncode':'Valid'}]))
    else:
        return(json.dumps([{'Retuen':'Success','Returncode':'InValid'}]))
    
def CheckConfirmationmobile(request):
    try:
        conf = request.json['confirmation']
        mobile = request.json['mobile']
        sql = json.loads(dbget("select customer_amount from ivr_room_customer_booked \
                               where customer_confirmation_number = '"+str(conf)+"' \
                               and customer_mobile = '"+str(mobile)+"'"))
        return json.dumps({'Return':'Success','Returncode':"Your Amount is "+str(sql[0]['customer_amount'])},indent=2)
    except:
          return json.dumps({'Return':'Failure','Returncode':"Record Does not exist"},indent=2)  


def check_phonenumber(request):
    number = request.json['mobile']
    if int(number.isdigit()) and len(number) == 10:
        print("Valid mobile number")
        return json.dumps([{"Return_Code":"Valid","ReturnValue":"Success"}],indent=4)
    else:
        print("Invalid mobile number")
        return json.dumps([{"Return_Code":"InValid","ReturnValue":"Failure"}],indent=4)

def CheckTotalnights(request):
  try:
        conf = request.json['confirmation']
        mobile = request.json['mobile']
        sql = json.loads(dbget("select nights from ivr_room_customer_booked \
                               where customer_confirmation_number = '"+str(conf)+"' \
                               and customer_mobile = '"+str(mobile)+"'"))
        return json.dumps({'Return':'Success','Returncode':"Your total number of  night's "+str(sql[0]['nights'])},indent=2)
  except:
         return json.dumps({'Return':'Failure','Returncode':"Record Does not exist"},indent=2)

def get_statuscount(request):
    mobile = request.args['mobile']
    print(mobile)
    sql = json.loads(dbget("select count(customer_booked_status) as reservation,(select count(modification) from public.ivr_room_customer_booked\
    where customer_mobile='"+str(mobile)+"'and modification in ('yes','Yes') group by modification) as modificationcount,(select count(customer_booked_status)\
    from public.ivr_room_customer_booked where customer_booked_status = 'cancel' and customer_mobile='"+str(mobile)+"') as cancel from public.ivr_room_customer_booked\
    where customer_mobile='"+str(mobile)+"' and  customer_booked_status = 'booked'\
    group by customer_booked_status"))
    psql = sql[0]
    dic = {"reservation":psql['reservation'] if psql['reservation'] is not None else 0,
           "modification":psql['modificationcount'] if psql['modificationcount'] is not None else 0,
           "cancel":psql['cancel'] if psql['cancel'] is not None else 0}
    
    return json.dumps({'Return':'Success','ouput':dic},indent=2)

def graphical_rep():
    
 
# Data to plot
    labels = 'Reservation', 'Modification', 'Cancel'
    sizes = [50, 10, 2]
    colors = ['gold', 'yellowgreen', 'lightcoral']
    explode = (0.1, 0, 0)  # explode 1st slice
     
    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
     
    plt.axis('equal')
    plt.show()
    plt.savefig('mygraph.png')
    


