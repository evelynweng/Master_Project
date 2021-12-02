'''
Between Mobilapp and cloudservice
store_id=1, store_name="KFC", store_phone =' 12345678', password = 'testpwd'
keyvalue same as database column
'''
# system
localadd = "http://localhost:8080/"
awsadd = "http://13.52.180.123:8080/"
selectnet = localadd
sys_API_LOCATION = selectnet + "cloudservice/"
sys_Q_API_LOCATION = selectnet + "queueweb/"
sys_DATABASE_API_LOCATION =  selectnet + "apidatabase/"

# key for dict:
kVALID = 'CMPE295'

kREPLY = 'REPLY'
keyReply = 'REPLY'

kSERVICE = 'SERVICE'
keyService = 'SERVICE'

kSTOREID = 'store_id'
keyStoreid = 'store_id'

kMASKPIC = 'mask_pic' # if vaccination card == true, mask pic will be vaccination card. 
keyMaskpic = 'mask_pic'

kQRCODE = 'QRCODE'
keyQrcode = 'QRCODE'

kSTOREPHONE ='store_phone'
kPASSWORD = 'password'
kSTORENAME = 'store_name'
kSTORECAPACITY ='store_capacity'

kSTOREINOUT = 'store_in_out'
kGET_TEMP_REQ = 'temp_request'
kTEMP_DATA = 'temp_data'

kCUSTOMERNUMBERS = 'customer_numbers' # for queue app
kCUSTOMERID = "customer_id"
kVACCINATION = 'vacc_card' # for have vaccination card

# values for dict:
vVALID = 295

# SERVICE value
vLOGIN = 'LOGIN'
vREGISTER = 'REGISTER'
vMASK = 'MASK'
vCHECKIN ='CHECKIN'
vSTARTDETECT = 'STARTDETECT'

vSTOREINOUT = 'store_in_out'
vGET_TEMP_REQ = 'temp_request'
vTEMP_DATA = 'temp_data'

# To queue system
vQUERYCAPACITY = 'ENTRY'
vLEAVE = 'LEAVE'

# value for PIR sensor - store in/out
vSTOREIN = 'True'
vSTOREOUT = 'False'

# kSERVICE value to queue web application
# might not use in future
qrCode = 'QRCODE'