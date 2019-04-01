from sqlwrapper import gensql,dbget
import json
import datetime
from decimal import Decimal
import math

def calculatetotalcharges(request):
    #try:
        if request.method == 'GET':
                d = {}
                tfn = '+'+request.args['tfn_num']
                customer_adult = request.args['adult']
                customer_child = request.args['child']
                customer_arrival_date = request.args['arrival_date']
                customer_depature_date = request.args['depature_date']
                customer_room_type = request.args["room_type"] # ROOM_ID
        if request.method == 'POST':
                tfn = request.json['tfn_num']
                customer_adult = request.json["adult"]
                customer_child = request.json["child"]
                customer_arrival_date = request.json["arrival_date"]
                customer_depature_date = request.json["depature_date"]
                customer_room_type = request.json["room_type"] # ROOM_ID
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
        #customer_arrival_date = request.json["arrival_date"]
        #customer_depature_date = request.json["depature_date"]
        #customer_room_type = request.json["room_type"] # ROOM_ID
        print(customer_room_type,type(customer_room_type))
       # customer_room_type = customer_room_type.title()
       # print("roomtype",customer_room_type)
        #customer_adult = request.json["adult"]
        #customer_child = request.json["child"]
        print("adults",customer_adult,type(customer_adult))
        d,e,d1,d2 = {},[],{},{}
        print(customer_arrival_date,customer_depature_date)
        today_date = datetime.datetime.utcnow().date()
        year = str(today_date.year)
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
        
        print("arrival",customer_arrival_date,"depature",customer_depature_date,"roomid",customer_room_type,"businessid",bi_id[0]['business_id'])    # CONFIGRATION
        sql = json.loads(dbget("select max_extra_bed.extrabed,extranet_availableroom.extra_adult_rate,extranet_availableroom.rate_plan_id,extranet_availableroom.room_date,extranet_availableroom.room_rate,configration.max_adults \
                                    from configration \
                                   join extranet_availableroom on extranet_availableroom.room_id = configration.room_id \
                                   join max_extra_bed on max_extra_bed.extrabed_id = configration.maximum_extrabed_id \
                                   where configration.room_id  = '"+str(customer_room_type)+"' and configration.business_id='"+bi_id[0]['business_id']+"'and extranet_availableroom.room_date between '"+str(customer_arrival_date)+"' and '"+str(customer_depature_date)+"'"))
        #print("res",result)
     
        #available_rate = json.loads(dbget("select room_id,room_rate,room_date,rate_plan_id from extranet_availableroom where room_date between '"+str(customer_arrival_date)+"' and '"+str(customer_depature_date)+"' and room_id='"+str(customer_room_type)+"'"))
        #print(available_rate)
        s = 0
        total_adult = int(customer_adult)
        max_adult = int(sql[0]['max_adults'])
        extra_bed = int(sql[0]['extrabed'])
        extra_adult_rate = sql[0]['extra_adult_rate']
        rooms_rate =  int(sql[0]['room_rate'])
        
        plan_rate = int(sql[0]['rate_plan_id'])

        print("plan_rate",plan_rate)
        total_beds = max_adult + extra_bed
        total_rooms = total_adult / total_beds
        total_rooms_count = math.ceil(total_rooms)
        print(total_rooms_count)
        
    
        sumva = 0
        for i in sql:
                arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d')
                depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d')
                conf_date = datetime.datetime.strptime(i['room_date'], '%Y-%m-%d')
                print("conf_date",conf_date)
                deltadates = depature_date - arrival_date
                for x in range(deltadates.days + 1):
                   #print(arrival_date + datetime.timedelta(i))
                   datebetween = arrival_date + datetime.timedelta(x)
                   if datebetween == conf_date and plan_rate == int(i['rate_plan_id']) :
                      
                      print(i["extra_adult_rate"],i['room_rate'],i['room_rate'])
                      r1 = max_adult * total_rooms_count
                      extra_price = (int(customer_adult) - r1) * int(i["extra_adult_rate"])
                      price = total_rooms_count * int(i['room_rate'])
                      total = price + extra_price                        
                      sumva += total
                      ##price1 = result1 * int(i['room_rate'])
                      

                      
                      #price2 = (total_adult - result1) * (int(i["extra_adult_rate"])+int(i['room_rate']))
                       #datebetween.strftime('%d %B')
                      datelist_rate.append({"day":datebetween.strftime('%Y-%m-%d'),"total":total})
                      #print(datelist_rate)
                   
              
        print(datelist_rate)
        print("sumva",sumva)
       
        
        
        def myconverter(o):
                    if isinstance(o, datetime.datetime):
                         return o.__str__()  
 
        return(json.dumps({"ServiceMessage":"Success","Total_Amount":sumva,"date_amount":datelist_rate},indent=2,default=myconverter))
        
        #return(json.dumps({"ServiceMessage":"Success","Total_Amount":total_amout,"date_month_amount":last_list},indent=2))
        
    #except:
       # return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"}))
