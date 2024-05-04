from django.contrib import admin
from django.urls import path
from.import views,place_order,get_trade,history,margin,LTP,individual_order,get_order,update_order_status,orderonltp,marketprice,exits,profitloss,theme
from .place_order import *
from .get_trade import *
from .margin import *
from .LTP import *
from .individual_order import *
from .get_order import *
from .update_order_status import *
from .orderonltp import *



urlpatterns = [
    path('viewdetails/',views.get_details.as_view(),name="viewdeatils"),
    path('gettradebook/',views.get_trade_book.as_view(),name='gettradebook'),
    path('get_real_time_data/',views.real_time_data.as_view(),name='real_time_data'),
    path('NSE_real_time_data/',views.NSE_real_time_data.as_view(),name='NSE_real_time_data'),
    path('NSE_option_chain_data_check/<str:symbol>/',views.NSE_option_chain_data_check.as_view(),name='NSE_option_chain_data_check'),
    path('NSE_option_chain_data/',views.NSE_option_chain_data.as_view(),name='NSE_option_chain_data'),
    path('NSE_company_name/',views.NSE_company_name.as_view(),name='NSE_company_name'),
    path('OptionsData/<str:symbol>/',views.OptionsData.as_view(),name='OptionsData'),
    path('Order_placing/',views.Order_placing.as_view(),name='Order_placing'),
    path('ExpiryStrikePrice/<str:symbol>/',views.ExpiryStrikePrice.as_view(),name="ExpiryStrikePrice"),
    path('ExpiryStrikeData/<str:symbol>/',views.ExpiryStrikeData.as_view(),name='ExpiryStrikeData'),
   
    path('based_on_expiry_date/<str:symbol>/',views. based_on_expiry_date.as_view(),name=' based_on_expiry_date'),
    path('GetTradeBookAPIView/',get_trade.GetTradeBookAPIView.as_view(),name='GetTradeBookAPIView'),
    path('Tradingsymbol_token/',views.Tradingsymbol_token.as_view(),name=" Tradingsymbol_token"),
    path('NSE_Tradingsymbol_token/',views.NSE_Tradingsymbol_token.as_view(),name='NSE_Tradingsymbol_token'),
    path('Historical_data/',history.Historical_data.as_view(),name="Historical_data"),##### sample for get history data and find the P/L
    #############################################################################################################
    path('OrderPlacementAPIView/',place_order.PlaceOrderAPIView.as_view(),name='OrderPlacementAPIView'),######order placing by giving manual value
    path("GetOrderBook/",get_order.GetOrderBook.as_view(),name="GetOrderBook"),#### it gives all leg response,text,status,uniqueorderid
    path("ProfitLossAPIView/",history.ProfitLossAPIView.as_view(),name="ProfitLossAPIView"),### find the P/L for each and all leg
    path('IndividualOrderStatus/<str:uniqueorderid>/',individual_order.IndividualOrderStatus.as_view(),name='IndividualOrderStatus'),###### based on uniqueorderid it gives particular leg response,status,text,uniqueorderid
    path('multiple_legs/',views.MultipleLegs.as_view(),name="multiple_legs"),##### sample code for multiple leg
    path('MarginCalculatorAPI/',margin.MarginCalculatorAPI.as_view(),name="MarginCalculatorAPI"),##### get all company details from margin calculator
    path('Companyname_expiry/',margin.Companyname_expiry.as_view(),name="Companyname_expiry"),#######based on  all company name it shows expiry date only
    path("Option_Data_CEPE/<str:company_name>/",margin.Option_Data_CEPE.as_view(),name="Option_Data_CEPE"),#### based on one company name send CE/PE to the frontend
    path("RetrieveLegFields/",views.RetrieveLegFields.as_view(),name="RetrieveLegFields"),##### based on  each strategy name send the legs to the front end 
    path("StrategyView/",views.StrategyView.as_view(),name="StrategyView"),##### store the strategy and leg details in database
    path("RetrieveStrategyByUserId/",views.RetrieveStrategyByUserId.as_view(),name="RetrieveStrategyByUserId"),#Here all data is sent to frontend, based on userid send the legs
    ################Authentication#########################################
    path("SignInUserAPIView/",views.SignInUserAPIView.as_view(),name="SignInUserAPIView"),##### signin for user
    path("EmailverifyOTP/",views.EmailverifyOTP.as_view(),name="EmailverifyOTP"),###### verifying user entered email by OTP
    path("Send_userdetail/",views.Send_userdetail.as_view(),name="Send_userdetail"),##### sample code for send user detil to frontend
    path("LoginAPIView/",views.LoginAPIView.as_view(),name="LoginAPIView"),#######user login
    path("ForgotPasswordAPIView/",views.ForgotPasswordAPIView.as_view(),name="ForgotPasswordAPIView"),#### forgot password
    path("ResetPasswordAPIView/",views.ResetPasswordAPIView.as_view(),name="ResetPasswordAPIView"),###reset password
    path("GetLtpData/",LTP.GetLtpData.as_view(),name="GetLtpData"),###### it gives detail of particular leg LTP(Last traded price),Low,High,Open,Close
    path("Option_Data_CEPE_expiry/",margin.Option_Data_CEPE_expiry.as_view(),name="Option_Data_CEPE_expiry"),#### based on company name,expirydate it gives CE/PE 
    path("Expiry_CEPEonly/",margin.Expiry_CEPEonly.as_view(),name="Expiry_CEPEonly"),##### sample code
    path('Userdetails/',views.user_details.as_view(),name='Userdetails'),######send user details front end
    path('StatusApiview/',views.status_view.as_view(),name='status_view'),####### based on status="active" Place the order,store orderid,uniqueorderid in leg database
    #########################To update order status###########
    path('Updateorder/',update_order_status.update_order.as_view(),name="update_order"), ####### every 45-seconds update the order status and reason in leg database

    path('Order_on_ltp/',orderonltp.Order_on_ltp.as_view(),name="Order_on_ltp"),
    path('Trigger_on_ltp/',orderonltp.trigger_on_ltp.as_view(),name="Trigger_on_ltp"),

    ##########To add on Nse symboltoken to company names############
    path('MarketpriceAPIView/',marketprice.MarketpriceAPIView.as_view(),name="MarketpriceAPIView"),

    path("squareofff/",orderonltp.squareofff.as_view(),name="squareofff"),

    path("exitontrigger/",exits.ExitOnTrigger.as_view(),name="exitontrigger"),

    path("orderonprice/",exits.OrderOnprice.as_view(),name="orderonprice"),

    path("exitonstoploss/",exits.ExitOnstoploss.as_view(),name="exitonstoploss"),

    path("exitwhereitis/",exits.ExitwhereItis.as_view(),name="exitwhereitis"),

    path("getpl/",profitloss.sendpl.as_view(),name="getpl"),
    ###########Asynchronous#########

    path("cancel_delete/",profitloss.CancelAPI.as_view(),name="cancel_delete"),

    path("delete_strategy/",profitloss.DeleteStrategy.as_view(),name="delete_strategy"),

    path("checkpl/",profitloss.checkpl.as_view(),name="checkpl"),

    path("ThemeView/",theme.ThemeView.as_view(),name="ThemeView"),

    path('ThemeRetrive/',theme.ThemeRetrive.as_view(),name="ThemeRetrive")
]
