import json
from sqlwrapper import gensql

def updatecustomerlangselected(request):
    ani = request.args["ani"]
    lang = request.args["lang"]
    d = {}
    d['customer_ani'] = ani
    tab1 = (gensql('select','ivr_customer_profile','customer_language_pref',d))

    if len(tab1) > 2 :
        print(tab1)
        return(json.dumps({"Return":"Language Already Selected","Return_Code":"LAS","Status": "Success",
                      "Status_Code": "200"},indent=2))
    d['customer_language_pref'] = lang
    result = gensql('insert','ivr_customer_profile',d)
    
    return(json.dumps({"Return":"Record Inserted Successfully","Return_Code":"RIS","Status": "Success",
                      "Status_Code": "200"},indent=2))

