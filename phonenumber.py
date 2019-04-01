import phonenumbers
import json
def phonenumbers_country(request):
  try:   
   phone = request.json['phone']
   tstl = phonenumbers.parse(phone,None)
   print(tstl.country_code)
   print(tstl.national_number)
   countrycode = tstl.country_code
   national_number = tstl.national_number
   return (json.dumps({'Status':'Success', 'Returnvalue_country': countrycode, 'Returnvalue_Nationalnumber': national_number}, indent =4))
  except:
   return (json.dumps({'Status':'Failure'}, indent =4))   
      
