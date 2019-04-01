from sqlwrapper import dbget,gensql,dbput
import json
import datetime
from dateutil import parser
def fetchroomsavailabilityandprice(request):
    #try:
        if request.method == 'GET':
            d = {}
            print("hii")
            tfn = '+'+request.args['TFN']
            print("tfn",tfn)
            d['adult'] = request.args['adult']
            d['child'] = request.args['child']
            arr = request.args['arrival_date']
            dep = request.args['depature_date']
        if request.method == 'POST':
            d = request.json
            print(d)
            tfn = request.json['TFN']
            adult = d['adult']
            child = d['child']
            arr = d['arrival_date']
            dep = d['depature_date']
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id)#,b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))

        
        #arr = d['arrival_date']
        #dep = d['depature_date']
        customer_arrival_date = parser.parse(arr).date().strftime('%Y-%m-%d')
        customer_depature_date = parser.parse(dep).date().strftime('%Y-%m-%d')
        customer_arrival_date = datetime.datetime.strptime(customer_arrival_date, '%Y-%m-%d').date()
        customer_depature_date = datetime.datetime.strptime(customer_depature_date, '%Y-%m-%d').date()

        today_date = datetime.datetime.utcnow().date()
        if customer_arrival_date < today_date:
                customer_arrival_date = customer_arrival_date+datetime.timedelta(days=365)
        if customer_depature_date < today_date:
                customer_depature_date = customer_depature_date+datetime.timedelta(days=365)
                    
        print("arr",customer_arrival_date)
        print("dep",customer_depature_date)
                 
        
        d['customer_arrival_date'] = customer_arrival_date
        d['customer_depature_date'] = customer_depature_date

        
        #nights = customer_depature_date.day - customer_arrival_date.day
        
        #print("nights",customer_arrival_date,type(customer_arrival_date))
        if customer_arrival_date != customer_depature_date:
            d['customer_depature_date'] = customer_depature_date - datetime.timedelta(days=1)

        print("d['customer_depature_date']",d['customer_depature_date'])

        
        room_to_sell = json.loads(dbget("select * from room_to_sell where room_date between '"+str(d['customer_arrival_date'])+"'\
                                         and '"+str(d['customer_depature_date'])+"' and business_id='"+bi_id[0]['business_id']+"' "))
        
        #print(room_to_sell,type(room_to_sell))
        
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
              return(json.dumps({"total":{'room_name0':"No Rooms Available For Given Date"},
                                 "Return_Code":"RRS", "Status": "Success",
                                 "Status_Code": "200"},indent=2))          
        rates = json.loads(dbget("select extranet_availableroom.room_id, configration.room_name, room_date,\
                                  room_rate,extranet_availableroom.extra_adult_rate,\
                                  room_open, extranet_availableroom.rate_plan_id from extranet_availableroom \
                                  join configration on extranet_availableroom.room_id = configration.room_id where\
                                  room_date between \
                                  '"+str(d['customer_arrival_date'])+"' and '"+str(d['customer_depature_date'])+"' and \
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
                    
                if tol['room_id'] == bed['room_id']:    
                   #print(tol,"1111111111111111111111111111111")
                   total_bed = bed['total_bed']
                   extrabed = bed['extrabed']
                   rate_plan = tol['rate_plans']
                   for plan in rate_plan:
                        room_rate, extra_adult_rate =[],[] 
                        for p in plan:
                            room_rate.append(p['room_rate'])
                            extra_adult_rate.append(p['extra_adult_rate'])
                        r1 = min(room_rate)+min(extra_adult_rate)
                        #print(r1)
                        add_amount.append(r1)
                   amount['amount'+""+str(count)+""] = sum(add_amount)     
                   #amount['room_id'+""+str(count)+""] = bed['room_id']
                   amount['room_name'+""+str(count)+""] = bed['room_name']
                   count += 1
            final.append(amount)
    
        #print(total)
        #print(add_amount)
        amount['count'] = count
        #print("final",final,amount)
        return(json.dumps({"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success","Status_Code": "200","total":amount},indent=2))   
    
def fetchpromotionalmessage(request):
    try: 
        today_date = datetime.datetime.utcnow().date()
        tfn = request.json['TFN']
        
        b_id = json.loads(dbget("select id from ivr_dialed_number where dialed_number='"+tfn+"' "))
        print(b_id[0]['id'])
        bi_id = json.loads(dbget("select business_id from ivr_hotel_list where id='"+str(b_id[0]['id'])+"' "))
        print(bi_id[0]['business_id'],type(bi_id[0]['business_id']))
        id1 = json.loads(dbget("select id from ivr_hotel_list where business_id='"+bi_id[0]['business_id']+"' "))
        #print(id1[0]['id'])
        date = json.loads(dbget("select message_date_start,message_date_end from \
                                ivr_promotional_message where id="+str(id1[0]['id'])+" "))
        print(date)
        st_d = date[0]['message_date_start']
        ed_d = date[0]['message_date_end']
        st_d = datetime.datetime.strptime(st_d,'%Y-%m-%d').date()
        ed_d = datetime.datetime.strptime(ed_d,'%Y-%m-%d').date()
        print(st_d,ed_d,type(st_d))
        #today_date = '2018-05-01'
        #today_date = datetime.datetime.strptime(today_date,'%Y-%m-%d').date()
        print("today",today_date)
        if today_date <= ed_d  and today_date >= st_d:       
            result = json.loads(dbget("select message from ivr_promotional_message where id="+str(id1[0]['id'])+" "))
            #print(result)
            result = result[0]
            #return(json.dumps({"Return":"Record Retrieved Successfully","Return Code":"RRS", "Status": "Success",
             #                 "Status Code": "200", "Return Value":result},indent=2))
            dict1 = {"Return":"Record Retrieved Successfully","Return_Code":"RRS", "Status": "Success",
                              "Status_Code": "200"}
            print(dict1,type(dict1))
            dict1.update(result)
            print(dict1)
            return(json.dumps(dict1))
        else:
            return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))
    except:
        return(json.dumps({"ServiceStatus":"Success","ServiceMessage":"Failure"},indent=2))
def insertpromotionalmessage(request):
    #e = request.json
  try:  
    bus_id = request.json['business_id']
    message = request.json['message']
    st = request.json['message_date_start']
    ed = request.json['message_date_end']
    b_id = json.loads(dbget("select id from ivr_hotel_list where business_id='"+bus_id+"' "))
    print(b_id[0]['id'])
    count = json.loads(dbget("select count(*) from ivr_promotional_message where \
                              id='"+str(b_id[0]['id'])+"' "))
    print(count)
    e = {}
    e['message'] = message
    print(type(message))
    e['id'] = b_id[0]['id']
    e['message_date_start']= st
    e['message_date_end'] = ed
    if count[0]['count'] != 1:
        print(gensql('insert','ivr_promotional_message',e))
    else:
            print(dbput("update ivr_promotional_message set message = '"+str(message)+"' , message_date_start = '"+st+"', message_date_end='"+ed+"' where id='"+str(b_id[0]['id'])+"' "))
    a = {"ServiceStatus":"Success","ServiceMessage":"Success"}
    return(json.dumps(a))
  except:
    a = {"ServiceStatus":"Success","ServiceMessage":"Failure"}
    return(json.dumps(a)) 
     
