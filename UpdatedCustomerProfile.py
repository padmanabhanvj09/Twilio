import json
from sqlwrapper import gensql

def updatedcustomerprofile(request):
    #customer_name = request.json['customer_name']
    customer_mobile = request.json['customer_mobile']
    
    #customer_email = request.json['customer_email']
    customer_email = "infocuit.daisy@gmail.com"
    customer_cc = request.json['customer_cc']
    customer_expirydate = request.json['customer_expirydate']
    customer_expirydate = customer_expirydate[0:2]+'/'+customer_expirydate[2:]
    
    customer_room_type = request.json['customer_room_type']
    customer_pickup_drop = request.json['customer_pickup_drop']
    #customer_menu_navigation = request.json['customer_menu_navigation']
    adults = request.json['adults']
    child = request.json['child']
    d1,d2,d3 = {},{},{}
    #d1['customer_name'] = customer_name
    d1['customer_mobile'] = customer_mobile
    d2['customer_email'] = customer_email
    d2['customer_cc'] = customer_cc
    d2['customer_expirydate'] = customer_expirydate
    d3['customer_expirydate'] = customer_expirydate
    d3['customer_cc'] = customer_cc
    d3['customer_room_type'] = customer_room_type
    d3['customer_pickup_drop'] = customer_pickup_drop
    d3['customer_adultsm'] = adults
    d3['customer_child'] = child
    #d3['customer_menu_navigation'] = customer_menu_navigation
    
    print(gensql('update','ivr_customer_profile',d2,d1))
    print(gensql('update','ivr_room_customer_booked',d3,d1))
    return(json.dumps({"Return":"Record Updated Successfully","Return Code":"RUS","Status": "Success",
                      "Status Code": "200"},indent=2))
