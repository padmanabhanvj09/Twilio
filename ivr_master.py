'''
This is the master file for all the Web services
related to IVR application
'''
import json
from flask import Flask,request, jsonify
from flask_cors import CORS
from QueryANITEST import queryanitest
from QueryANI import queryani
from UpdateCustomerLangSelected import updatecustomerlangselected
from FetchExistingBookings import fetchexistingbookings
from CancelCurrentbooking import cancelcurrentbooking
from FetchRoomsAvailabilityandPrice import fetchroomsavailabilityandprice
from FetchRoomsAvailabilityandPrice import fetchpromotionalmessage
from CalculateTotalChargesAndRetrieveConfirmationNumber import calculatetotalcharges
from UpdatedCustomerProfile import updatedcustomerprofile
from SendSMS import sendsms
from SendEmailIVR import sendemailivr
from gupshupproof import updategupshupreservation
##extranet
from SignupExtranet import signup
from LoginExtranet import login
from AvailableRoomCount import availableroomcount
from RoomList import roomlist
from RatesandAvailability import ratesandavailability
from InsertRatesandAvailability import insertratesandavailability
from UpdateRatesandAvailability import updateratesandavailability
from AddDiscount import adddiscount
from QueryDiscount import querydiscount

#add
from CheckDate import validationivr
from SendEmail import sendemail
from SendEmailANI import callexternalapi
from RatesInsertAndUpdate import ratesinsertandupdate
from UpdateExistingBooking import updateexistingbooking
from PromotionalCancelMessage import promotionalcancelmessage
from InsertCustomerRoomBooking import insertcustomerroombooking
from ValidateConfirmationNumber import validateconfirmationnumber
from FetchBooking import fetchbooking
#
from phonenumber import phonenumbers_country
from PromotionalCancelMessage import insertcancelmessage
from FetchRoomsAvailabilityandPrice import insertpromotionalmessage
from RoomList import insertroomlist
from InsertCancelPolicy import insertcancelpolicy
from InsertCancelPolicy import QueryStatistics
from Insert_Ivr_Reservation import Insert_Ivr_Reservation
from Getreservationcancelmodification import Getreservationcancelmodification
from Getchannelcount import Getchannelcounts
from Getreservationcancelmodification import GetBookingConfirmation
from SendSMS import UpdateSMSmessage
from SendSMS import Updateivrsmsmessage
from Getreservationcancelmodification import Getsmscount
from Getreservationcancelmodification import GetLanguagecount
from Getreservationcancelmodification import GetRoomOccupancy
from Getreservationcancelmodification import GetYearbyyeareservationcount
from Getreservationcancelmodification import GetCountryreservation
from Getreservationcancelmodification import monthreservation
from Getreservationcancelmodification import futurebooking
from Getreservationcancelmodification import HistoryBooking
from Getreservationcancelmodification import GetConvergencereport

from Inserttwilioreservation import Inserttwilioreservation
from Inserttwilioreservation import InsertArrivalDeparture
from Inserttwilioreservation import Modifytwilioreservation
from Inserttwilioreservation import Canceltwilioreservation
from Inserttwilioreservation import Smstwilioservice
from Inserttwilioreservation import CheckConfirmation
from InsertCustomerRoomBooking import checkinguest

from Inserttwilioreservation import twiliofetchroomsavailabilityandprice
from Inserttwilioreservation import twiliocalculatetotalcharges
from Inserttwilioreservation import CheckRoomtype
from Inserttwilioreservation import CheckConfirmationmobile
from Inserttwilioreservation import check_phonenumber
from Inserttwilioreservation import CheckTotalnights
from Inserttwilioreservation import graphical_rep
from Inserttwilioreservation import get_statuscount
# add changes
from RatesandAvailability import daterange
from RoomList import restriction
from configuration import config
from configuration import select_config
from configuration import update_config
from Insert_Ivr_Reservation import Query_Reservation
from RoomList import select_restriction
from create_rate_plan import select_rateplanid
from RatesandAvailability import room_open_update
from Insert_Ivr_Reservation import Query_Rate_Per_day
from RatesandAvailability import room_to_sell_update

from SendEmailWhatsapp import sendemailwhatsapp
from ImageUploadS3 import upload_file
from ImageUploadS3 import get_aws_keys

#Rate_plan
from create_rate_plan import select_room_types
from create_rate_plan import select_cancellation_policy
from create_rate_plan import select_packages
from create_rate_plan import create_rate_plan
from create_rate_plan import update_rate_plan
from create_rate_plan import delete_rate_plan
from create_rate_plan import select_rate_plan
from create_rate_plan import select_plan
from create_rate_plan import Insert_Packages
#SignUp

from User_signup import User_signup
from User_signup import User_login
from User_signup import Business_signup

#configuration
from ExtranetConfiguration import RoomsizeConfiguration
from ExtranetConfiguration import BeddingoptionsConfiguration
from ExtranetConfiguration import BedsizeConfiguration
from ExtranetConfiguration import RoomamenitieConfiguration
from ExtranetConfiguration import InclusionsConfiguration
from ExtranetConfiguration import DeleteRoomsizeConfiguration
from ExtranetConfiguration import DeleteBeddingoptionsConfiguration
from ExtranetConfiguration import DeleteBedSizeConfiguration
from ExtranetConfiguration import DeleteInclusionsConfiguration
from ExtranetConfiguration import DeleteRoomamenitieConfiguration
from ExtranetConfiguration import RoomnameConfiguration
from ExtranetConfiguration import SelectRoomsizeConfiguration
from ExtranetConfiguration import SelectBeddingoptionsConfiguration
from ExtranetConfiguration import SelectBedsizeConfiguration
from ExtranetConfiguration import SelectRoomamenitieConfiguration
from ExtranetConfiguration import SelectInclusionsConfiguration
from ExtranetConfiguration import SelectExtrabed
from sendemailconfirmation import sendemailconfirmation

#Dashobos
from DashboardReport import Lastreportrecord
from DashboardReport import lastreservationcount
from DashboardReport import lastchannelrecord



app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
   return "Welcome to IVR!"
@app.route('/QueryANI/test',methods=['GET'])
def QueryANITest():
   return queryanitest(request)

@app.route('/QueryANI',methods=['GET','POST'])
def QueryANIinfo():
   return queryani(request)
@app.route('/UpdateCustomerLangSelected',methods=['GET'])
def LangSelected():
   return updatecustomerlangselected(request)
@app.route('/FetchExistingBookings',methods=['GET','POST'])
def ExistingBookings():
   return fetchexistingbookings(request)
@app.route('/CancelCurrentbooking',methods=['GET'])
def Cancelbooking():
   return cancelcurrentbooking(request)
@app.route('/FetchRoomsAvailabilityandPrice',methods=['GET','POST'])
def FetchRooms():
   return fetchroomsavailabilityandprice(request)
@app.route('/FetchPromotionalMessage',methods=['GET','POST'])
def FetchPromotionalMessage():
   return fetchpromotionalmessage(request)
@app.route('/CalculateTotalCharges',methods=['POST','GET'])
def CalculateTotalCharges():
   return calculatetotalcharges(request)
@app.route('/UpdatedCustomerProfile',methods=['POST'])
def UpdatedProfile():
   return updatedcustomerprofile(request)
@app.route('/SendSMS',methods=['POST'])
def SMS():
   return sendsms(request)
@app.route('/SendEmailIVR',methods=['POST'])
def Email():
   return sendemailivr(request)
##extranet
@app.route('/SignupExtranet',methods=['POST'])
def ExSignup():
   return signup(request)
@app.route('/LoginExtranet',methods=['POST'])
def ExLogin():
   return login(request)
@app.route('/AvailableRoomCount',methods=['POST'])
def ExAvailableRoomCount():
   return availableroomcount(request)
@app.route('/RoomList',methods=['POST'])
def ExRoomList():
   return roomlist(request)
@app.route('/RatesandAvailability',methods=['POST'])
def ExRatesandAvailability():
   return ratesandavailability(request)
@app.route('/InsertRatesandAvailability',methods=['POST'])
def ExInsertRatesandAvailability():
   return insertratesandavailability(request)
@app.route('/UpdateRatesandAvailability',methods=['POST'])
def ExUpdateRatesandAvailability():
   return updateratesandavailability(request)
@app.route('/AddDiscount',methods=['POST'])
def Discount():
   return adddiscount(request)
@app.route('/QueryDiscount',methods=['POST'])
def QueryDiscount():
   return querydiscount(request)
#add
@app.route('/ValidationIVR',methods=['POST'])
def CheckDate():
   return validationivr(request)
@app.route('/SendEmail',methods=['POST'])
def  sendemailmessage():
   return sendemail(request)
@app.route('/SendEmailANI',methods=['POST'])
def sendanimessage():
   return callexternalapi(request)
@app.route('/RatesInsertAndUpdate',methods=['POST'])
def RatesInsertAndUpdate():
   return ratesinsertandupdate(request)
@app.route('/UpdateExistingBooking',methods=['POST'])
def UpdateExistingBooking():
   return updateexistingbooking(request)
@app.route('/PromotionalCancelMessage',methods=['POST'])
def PromotionalCancelMessage():
   return promotionalcancelmessage(request)
@app.route('/InsertCustomerRoomBooking',methods=['POST'])
def InsertCustomerRoomBooking():
   return insertcustomerroombooking(request)
@app.route('/ValidateConfirmationNumber',methods=['POST'])
def ValidateConfirmationNumber():
   return validateconfirmationnumber(request)
@app.route('/FetchBooking',methods=['POST'])
def FetchBooking():
   return fetchbooking(request)
#
@app.route('/Phonenumbers',methods=['POST'])
def Phonenumbers():
   return phonenumbers_country(request)
@app.route('/InsertCancelMessage',methods=['POST'])
def InsertCancelMessage():
   return insertcancelmessage(request)
@app.route('/InsertPromotionalMessage',methods=['POST'])
def InsertPromotionalMessage():
   return insertpromotionalmessage(request)
@app.route('/InsertRoomList',methods=['POST'])
def InsertRoomList():
   return insertroomlist(request)
@app.route('/InsertCancelPolicy',methods=['POST'])
def InsertCancelPolicy():
   return insertcancelpolicy(request)
@app.route('/QueryStatistics',methods=['POST'])
def QueryStatisticsRecord():
   return QueryStatistics(request)
@app.route('/Insert_Ivr_Reservations',methods=['POST'])
def Insert_Ivr_Reservationswer():
   return Insert_Ivr_Reservation(request)
@app.route('/Getreservationcancelmodification',methods=['POST'])
def dashboarddetails():
   return Getreservationcancelmodification(request)
@app.route('/Getchannelcounts',methods=['POST'])
def Getchannelcounts_all():
   return Getchannelcounts(request)
@app.route('/GetBookingConfirmation',methods=['POST'])
def GetBookingConfirmation_all():
   return GetBookingConfirmation(request)

@app.route('/UpdateSMSmessage',methods=['POST'])
def UpdateSMSmessage_all():
   return UpdateSMSmessage(request)

@app.route('/Updateivrsmsmessage',methods=['POST'])
def Updateivrsmsmessage_all():
   return Updateivrsmsmessage(request)
@app.route('/Getsmscount',methods=['POST'])
def Getsmscount_all():
   return Getsmscount(request)
@app.route('/GetLanguagecount',methods=['POST'])
def GetLanguagecount_all():
   return GetLanguagecount(request)
@app.route('/GetRoomOccupancyall',methods=['POST'])
def GetRoomOccupancy_all():
   return GetRoomOccupancy(request)

@app.route('/GetYearbyyeareservationcount',methods=['POST'])
def GetYearbyyeareservationcount_all():
   return GetYearbyyeareservationcount(request)

@app.route('/GetCountryreservation',methods=['POST'])
def GetCountryreservation_all():
   return GetCountryreservation(request)

# add changes

@app.route('/daterange',methods=['POST'])
def daterangeforrates():
   return daterange(request)

@app.route('/restriction',methods=['POST'])
def restriction_rates():
   return restriction(request)

@app.route('/insert_configuration',methods=['POST'])
def insert_configuration():
   return config(request)

@app.route('/select_configuration',methods=['POST'])
def select_configuration():
   return select_config(request)

@app.route('/update_configuration',methods=['POST'])
def update_configuration():
   return update_config(request)

@app.route('/Query_Reservation',methods=['POST','GET'])
def Query_Reservation_Data():
   return Query_Reservation(request)

@app.route('/monthreservation',methods=['POST'])
def monthreservation_all():
   return monthreservation(request)

@app.route('/select_restriction',methods=['POST'])
def select_data_restriction():
   return select_restriction(request)
@app.route('/futurebooking',methods=['POST'])
def future_reservation():
   return futurebooking(request)
@app.route('/HistoryBooking',methods=['POST'])
def HistoryBooking_reservation():
   return HistoryBooking(request)
@app.route('/GetConvergencereport',methods=['POST'])
def GetConvergencereport_all():
   return GetConvergencereport(request)
@app.route('/Checkinguest',methods=['POST'])
def Checkinguest_all():
   return checkinguest(request)
@app.route('/select_room_types',methods=['POST'])
def select_roomtypes():
   return select_room_types(request)

@app.route('/select_cancellation_policy',methods=['POST'])
def select_cancelpolicy():
   return select_cancellation_policy(request)

@app.route('/select_packages',methods=['POST'])
def select_package():
   return select_packages(request)

@app.route('/create_rate_plan',methods=['POST'])
def create_rateplan():
   return create_rate_plan(request)

@app.route('/update_rate_plan',methods=['POST'])
def update_rateplan():
   return update_rate_plan(request)

@app.route('/delete_rate_plan',methods=['POST'])
def delete_rateplan():
   return delete_rate_plan(request)

@app.route('/select_rate_plan',methods=['POST'])
def select_rateplan():
   return select_rate_plan(request)

@app.route('/select_rateplanid',methods=['POST'])
def selectrateplanid():
   return select_rateplanid(request)

@app.route('/select_plan',methods=['POST'])
def selectplan():
   return select_plan(request)
@app.route('/Insert_Packages',methods=['POST'])
def Insert_Packages_all():
   return Insert_Packages(request)

#configuration
@app.route('/RoomsizeConfiguration',methods=['POST'])
def RoomsizeConfiguration_all():
   return RoomsizeConfiguration(request)
@app.route('/BeddingoptionsConfiguration',methods=['POST'])
def BeddingoptionsConfiguration_all():
   return BeddingoptionsConfiguration(request)
@app.route('/BedsizeConfiguration',methods=['POST'])
def BedsizeConfiguration_all():
   return BedsizeConfiguration(request)
@app.route('/RoomamenitieConfiguration',methods=['POST'])
def RoomamenitieConfiguration_all():
   return RoomamenitieConfiguration(request)
@app.route('/InclusionsConfiguration',methods=['POST'])
def InclusionsConfiguration_all():
   return InclusionsConfiguration(request)
@app.route('/DeleteRoomsizeConfiguration',methods=['POST'])
def DeleteRoomsizeConfiguration_all():
   return DeleteRoomsizeConfiguration(request)
@app.route('/DeleteBeddingoptionsConfiguration',methods=['POST'])
def DeleteBeddingoptionsConfiguration_all():
   return DeleteBeddingoptionsConfiguration(request)
@app.route('/DeleteBedSizeConfiguration',methods=['POST'])
def DeleteBedSizeConfiguration_all():
   return DeleteBedSizeConfiguration(request)
@app.route('/DeleteInclusionsConfiguration',methods=['POST'])
def DeleteInclusionsConfiguration_all():
   return DeleteInclusionsConfiguration(request)
@app.route('/DeleteRoomamenitieConfiguration',methods=['POST'])
def DeleteRoomamenitieConfiguration_all():
   return DeleteRoomamenitieConfiguration(request)
@app.route('/RoomnameConfiguration',methods=['POST'])
def Roomname():
   return RoomnameConfiguration(request)
@app.route('/SelectRoomsizeConfiguration',methods=['POST'])
def SelectRoomsizeConfiguration_all():
   return SelectRoomsizeConfiguration(request)
@app.route('/SelectBeddingoptionsConfiguration',methods=['POST'])
def SelectBeddingoptionsConfiguration_all():
   return SelectBeddingoptionsConfiguration(request)
@app.route('/SelectBedsizeConfiguration',methods=['POST'])
def SelectBedsizeConfiguration_all():
   return SelectBedsizeConfiguration(request)
@app.route('/SelectRoomamenitieConfiguration',methods=['POST'])
def SelectRoomamenitieConfiguration_all():
   return SelectRoomamenitieConfiguration(request)
@app.route('/SelectInclusionsConfiguration',methods=['GET'])
def SelectInclusionsConfiguration_all():
   return SelectInclusionsConfiguration()
@app.route('/SelectExtrabed',methods=['POST'])
def SelectExtrabed_all():
   return SelectExtrabed(request)
@app.route('/Inserttwilioreservation',methods=['POST','GET'])
def reservation():
   return Inserttwilioreservation(request)
@app.route('/InsertArrivalDeparture',methods=['POST','GET'])
def InsertArrivalDeparture_all():
   return InsertArrivalDeparture(request)


@app.route('/Modifytwilioreservation',methods=['POST','GET'])
def Modifytwilioreservation_all():
   return Modifytwilioreservation(request)
@app.route('/Canceltwilioreservation',methods=['POST','GET'])
def Canceltwilioreservation_all():
   return Canceltwilioreservation(request)
@app.route('/Smstwilioservice',methods=['POST','GET'])
def Smstwilioservice_all():
   return Smstwilioservice(request)
@app.route('/CheckConfirmation',methods=['POST','GET'])
def CheckConfirmation_all():
   return CheckConfirmation(request)
@app.route('/twiliofetchroomsavailabilityandprice',methods=['POST','GET'])
def twilio_fetchdetails():
   return twiliofetchroomsavailabilityandprice(request)
@app.route('/twiliocalculatetotalcharges',methods=['POST','GET'])
def twiliocalculatetotalcharges_show():
   return twiliocalculatetotalcharges(request)

@app.route('/CheckRoomtype',methods=['POST','GET'])
def CheckRoomtype_all():
   return CheckRoomtype(request)
#User_Signup

@app.route('/user_signup',methods=['POST'])
def user_signup():
   return User_signup(request)

@app.route('/User_login',methods=['POST'])
def Userlogin():
   return User_login(request)

@app.route('/Business_signup',methods=['POST'])
def business_signup():
   return Business_signup(request)

@app.route('/Dashboard_report',methods=['POST'])
def Lastreportrecord_all():
   return Lastreportrecord(request)

@app.route('/lastreservationcount',methods=['POST'])
def lastreservationcount_all():
   return lastreservationcount(request)
@app.route('/lastchannelrecord',methods=['POST'])
def lastchannelrecord_all():
   return lastchannelrecord(request)

@app.route('/update_room_open',methods=['POST'])
def update_roomopen():
   return room_open_update(request)

@app.route('/Query_Rate_Per_day',methods=['POST'])
def rate_per_day():
   return Query_Rate_Per_day(request)

@app.route('/sendemailwhatsapp',methods=['POST','GET'])
def emailwhatsapp():
   return sendemailwhatsapp(request)

@app.route('/upload', methods=['POST'])
def img():
   return upload_file(request)

@app.route('/get_aws_keys', methods=['POST'])
def aws_keys():
   return get_aws_keys(request)


@app.route('/sendemailconfirmation',methods=['POST'])
def sendemailconfirmation_all():
   return sendemailconfirmation(request)

@app.route('/room_to_sell_update',methods=['POST'])
def room_sell_update():
   return room_to_sell_update(request)
@app.route('/CheckConfirmationmobile',methods=['POST'])
def CheckConfirmation_All_mobile():
   return CheckConfirmationmobile(request)
@app.route('/check_phonenumber',methods=['POST'])
def check_phonenumber_all():
   return check_phonenumber(request)
@app.route('/CheckTotalnights',methods=['POST'])
def CheckTotalnights_al():
   return CheckTotalnights(request)

#-----------chart-----------------#
@app.route('/piechart',methods=['GET'])
def piechart_report():
   return graphical_rep()
#-------Count------------------#
@app.route('/gupshup_statuscount',methods=['GET'])
def statuscount():
   return get_statuscount(request)

#----------------gupshupproof----#
@app.route('/gupshup_proof',methods=['GET','POST'])
def imagegup():
   return updategupshupreservation(request)


if __name__ == "__main__":
   app.run(host="192.168.1.25",port=5000)
  #app.run(debug=True)
  
   
