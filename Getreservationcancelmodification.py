from sqlwrapper import gensql,dbget,dbput
import json
import datetime
from flask import Flask,request, jsonify
def Getreservationcancelmodification(request):
    
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
     
    business_id = request.json['business_id']
         
 
    ivreservationcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked')"))
    print(ivreservationcount)

    cancelcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"'  and customer_booked_status in ('canceled')"))
    print(cancelcount)

    
    
    Modificationcount = json.loads(dbget("select count(*) from ivr_room_customer_booked where business_id = '"+business_id+"' and  customer_arrival_date between '"+date_from+"' and '"+date_to+"'  and modification in ('yes')"))

    
    json_input = [
                   {"title":"Reservation","value":ivreservationcount[0]['count']},
                   {"title":"Cancel","value":cancelcount[0]['count']},
                   #{"title":"Totalbookingcount","value":Totalreservationcount[0]['count'] + totalivrcount[0]['count']},
                   {"title":"Modification","value":Modificationcount[0]['count']}
                   ]
  
   # json_input = {
      #          "title":["reservationcount","cancelcount","Totalbookingcount"],
       #         "value":[reservationcount[0]['count'] + ivreservationcount[0]['count'],cancelcount[0]['count'],Totalreservationcount[0]['count'] + totalivrcount[0]['count']]
                
       #         }
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
    
def GetBookingConfirmation(request):
    
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
     
    business_id = request.json['business_id']
    sql_value = json.loads(dbget("SELECT count(customer_confirmation_number) FROM public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"'  "))
    print(sql_value)

    ivreservationcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked') "))
    print(ivreservationcount)
    
    json_input = [
                   {"title":"Booking","value":ivreservationcount[0]['count']  },
                   
                   {"title":"Confirmation","value":sql_value[0]['count']}
                   ]
  
   # json_input = {
      #          "title":["reservationcount","cancelcount","Totalbookingcount"],
       #         "value":[reservationcount[0]['count'] + ivreservationcount[0]['count'],cancelcount[0]['count'],Totalreservationcount[0]['count'] + totalivrcount[0]['count']]
                
       #         }
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
def Getsmscount(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    business_id = request.json['business_id']
    ivreservationcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked')"))
    print(ivreservationcount)

    
    ivrsmscount = json.loads(dbget("select count(*) from ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and send_sms in ('success')"))
    print(ivrsmscount)
    json_input = [
                   {"title":"Booked","value":ivreservationcount[0]['count']  },
                   
                   {"title":"Delievered","value":ivrsmscount[0]['count'] }
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))

def GetLanguagecount(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
    business_id = request.json['business_id']
    arabic_count = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and ivr_language in ('1')"))
    print(arabic_count)
    ivr_englishcount = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and ivr_language in ('2')"))
    print(ivr_englishcount)
    
  
    json_input = [
                   {"title":"Arabic","value":arabic_count[0]['count']  },
                   
                   {"title":"English","value":ivr_englishcount[0]['count'] }
                   ]
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
def GetRoomOccupancy(request):
        d = request.json
        #print(d)
        dividendlist = []
        dividendlist_add = []
        date_from = request.json['arrival_from']
        date_to = request.json['arrival_to']
        
        business_id = request.json['business_id']
        if d['type'] == 1:
            res_type = 'customer_no_of_rooms'
        else:
            res_type = 'nights'
            
        ivr_room = json.loads(dbget("select customer_room_type,customer_no_of_rooms,nights from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' "))
        print(ivr_room)
        
        room_name = []
        new_ivr_room = []
        res = []
        for room in ivr_room:
            if room['customer_room_type']  in room_name:
                i = room_name.index(room['customer_room_type'])
            else:
                room_name.append(room['customer_room_type'])
                print("name",room_name)
                new_ivr_room.append([])
                i = room_name.index(room['customer_room_type'])
                
                
            new_ivr_room[i].append(room)
        print("newivr room",new_ivr_room)
        for rooms in new_ivr_room:

            res.append({"title":rooms[0]['customer_room_type'],
                       "value":sum(room[res_type] for room in rooms)})
            print(res)
                       
        #print(new_ivr_room)
        print(res)
        #print(room_name)
     
    
        return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":res},indent=2))
def GetYearbyyeareservationcount(request):
    business_id = request.json['business_id']
    yearlist = []
    dividendlist,dividendlist_add,fin_list  = [],[],[]
    count_of_year = {}
    Year1 = json.loads(dbget("select customer_arrival_date from public.ivr_room_customer_booked where business_id = '"+str(business_id)+"' order by customer_arrival_date"))
   
    for dividend_dict in Year1:
     for key, value in dividend_dict.items():
        dividendlist.append(value)
    
    year_count = 0
    for i in dividendlist:
        year_count = year_count+1
        j = datetime.datetime.strptime(i,'%Y-%m-%d').date()
        year_j = j.year
        sample = "'{}'".format(year_j)
        if sample in dividendlist_add:
            pass
        else: 
           dividendlist_add.append(sample)
           year_count = 1
        count_of_year[""+str(year_j)+""] = year_count

        
    print(count_of_year)
    #for key,value in count_of_year.items():
    for k,v in count_of_year.items():
        fin_list.append({'title':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)   
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":fin_list},indent=2))



def GetCountryreservation(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
  
    business_id = request.json['business_id']
    dividendlist_add ,count_of_year,fin_list= [],{},[]
    dividendlist,a,a_add,total_count,fin_list,cn_reservation  = [],[],[],{},[],[]

    ivr_country_count = json.loads(dbget("SELECT ivr_room_customer_booked.cntry_code, ivr_room_customer_booked.customer_no_of_rooms,ivr_room_customer_booked.nights ,country_list.country \
                                         from ivr_room_customer_booked \
                                         left join country_list on country_list.country_code = ivr_room_customer_booked.cntry_code where business_id = '"+business_id+"' and ivr_room_customer_booked.customer_arrival_date between '"+date_from+"' and '"+date_to+"'" ))
    
    
   # print("ivr",ivr_country_count)
    
    if request.json['type'] == 1:
            res_type = 'customer_no_of_rooms'
    else:
            res_type = 'nights'

    
    room_name = []
    new_ivr_room = []
    res = []
    for room in ivr_country_count:
            if room['country']  in room_name:
                i = room_name.index(room['country'])
            else:
                room_name.append(room['country'])
                print("name",room_name)
                new_ivr_room.append([])
                i = room_name.index(room['country'])
                
                
            new_ivr_room[i].append(room)
    print("newivr room",new_ivr_room)
    for rooms in new_ivr_room:

            res.append({"title":rooms[0]['country'],
                       "value":sum(room[res_type] for room in rooms)})
            print(res)
                       
        #print(new_ivr_room)
    print(res)
    

    
    '''
    for res in ivr_country_count:
        for k,v in res.items():
            if k == 'country':
                a.append(v)            
    print(a)
    country_count=0
    for cntry in ivr_country_count:
     for i in a:
        
        country_count = country_count+cntry[res_type]
        if i in a_add:
    
            pass
        else:
            a_add.append(i)
            country_count = cntry[res_type]
        total_count[""+str(i)+""] = country_count
    print(total_count)
    for k,v in total_count.items():
        fin_list.append({'title':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)
    '''
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":res},indent=2))

def monthreservation(request):
    year = request.json['year']
    dividendlist, dividendlist_add, count_of_year,fin_list = [],[],{},[]
    add_year = int(year)
    print(year,add_year)
    Year1 = json.loads(dbget("select customer_arrival_date from public.ivr_room_customer_booked  where  customer_arrival_date>='"+year+"-01-01' and customer_arrival_date<'"+str(add_year+1)+"-01-01' and customer_booked_status='booked' order by customer_arrival_date"))
    
    Year2 = json.loads(dbget("select arrival_date  from public.ivr_resevation  where arrival_date>='"+year+"-01-01' and arrival_date<'"+str(add_year+1)+"-01-01' order by arrival_date "))
    
    Year1 = Year1 + Year2
    
    for dividend_dict in Year1:
     for key, value in dividend_dict.items():
        dividendlist.append(value)
        
    year_count = 0
    for i in dividendlist:
        year_count = year_count+1
        j = datetime.datetime.strptime(i,'%Y-%m-%d').date()
        month_j = j.strftime("%b")
        sample = "'{}'".format(month_j)
        if sample in dividendlist_add:
            pass
        else: 
           dividendlist_add.append(sample)
           year_count = 1
        count_of_year[""+str(month_j)+""] = year_count

        
    print(count_of_year)
    for k,v in count_of_year.items():
        fin_list.append({'title':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":fin_list},indent=2))
def futurebooking(request):
    business_id = request.json['business_id']
    current_date = datetime.datetime.utcnow()
    current_date = current_date.date()
    #current_date = str(current_date)
    print(current_date)
    dividendlist, dividendlist_add, count_of_year,fin_list = [],[],{},[]
    
    
    Year1 = json.loads(dbget("select customer_arrival_date,customer_no_of_rooms,nights  from public.ivr_room_customer_booked  where  business_id = '"+business_id+"' and customer_arrival_date > '"+str(current_date)+"' and customer_booked_status='booked' order by customer_arrival_date"))
    
    

    print(Year1)
    if request.json['type'] == 1:
            res_type = 'customer_no_of_rooms'
    else:
            res_type = 'nights'
       
   
    year_count = 0
    for i in Year1:
        year_count = year_count + i[res_type]
        j = datetime.datetime.strptime(i['customer_arrival_date'],'%Y-%m-%d').date()
        month_j = j
        sample = "'{}'".format(month_j)
        if sample in dividendlist_add:
            pass
        else: 
           dividendlist_add.append(sample)
           year_count = i[res_type]
        count_of_year[""+str(month_j)+""] = year_count

        
    print(count_of_year)
    for k,v in count_of_year.items():
        fin_list.append({'date':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":fin_list},indent=2))

def HistoryBooking(request):
    business_id = request.json['business_id']
    current_date = datetime.datetime.utcnow()
    current_date = current_date.date()
    #current_date = str(current_date)
    print(current_date)
    dividendlist, dividendlist_add, count_of_year,fin_list = [],[],{},[]
    
    roomtype = {}
    Year1 = json.loads(dbget("select customer_arrival_date,customer_no_of_rooms,nights from public.ivr_room_customer_booked  where  business_id = '"+business_id+"' and  customer_arrival_date < '"+str(current_date)+"' and customer_booked_status='booked' order by customer_arrival_date"))

    
    print(Year1)
    if request.json['type'] == 1:
            res_type = 'customer_no_of_rooms'
    else:
            res_type = 'nights'
       
    year_count = 0
    print("came",res_type)
    for i in Year1:
        
        year_count = year_count + i[res_type]
        print("year_count",year_count)
        month_j = datetime.datetime.strptime(i['customer_arrival_date'],'%Y-%m-%d').date()
        sample = "'{}'".format(month_j)
        if sample in dividendlist_add:
            pass
        else: 
           dividendlist_add.append(sample)
           year_count = i[res_type]
        count_of_year[""+str(month_j)+""] = year_count
        print("count_of_year",count_of_year)

        
    #print(count_of_year)
    
    for k,v in count_of_year.items():
        fin_list.append({'date':k,'value':v})
        #fin_list.append(fin_res['value'] = v)
    print(fin_list)
    
        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":fin_list},indent=2))
def GetConvergencereport(request):
    date_from = request.json['arrival_from']
    date_to = request.json['arrival_to']
     
    business_id = request.json['business_id']
         
 
    booked = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"' and customer_booked_status in ('booked')"))
    print(booked)

    notbooked = json.loads(dbget("select count(*) from public.ivr_room_customer_booked where business_id = '"+business_id+"' and customer_arrival_date between '"+date_from+"' and '"+date_to+"'  and customer_booked_status in ('not booked')"))
    print(notbooked)

    json_input = [
                   {"title":"Booked","value":booked[0]['count']},
                   {"title":"Not Booked","value":notbooked[0]['count']}
                  
                   ]
  

        
    return(json.dumps({"Return":"Record Retrieved Sucessfully","Return_Code":"RTS","Status": "Success","Status_Code": "200","Returnvalue":json_input},indent=2))
