import imaplib, email, os, datetime

user = "m2dkcorreo@gmail.com"    #User name del correo al que queremos acceder
password = "12345678abcde"       #Contrasena del correo al que queremos acceder
imap_url = "imap.gmail.com"      #Algo que no se muy bien como funciona


connection = imaplib.IMAP4_SSL(imap_url)        #Conexion de tipo IMAP4 que provee python para poder hacer la verificacion con gmail
connection.login(user,password)                 #Conexion que toma como parametros el user creado anteriormente y la contrasena del correo
connection.list()
connection.select("INBOX")
                                                #print(connection.select('INBOX'))#Print para saber si me estoy conectando
#Esta funcion obtiene el cuerpo del mensaje, filtrando un poco de la informacion que obtiene la data completa
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
#fin funcion
result, data = connection.uid('search',None,"ALL")
i = len(data[0].split())
for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = connection.uid('fetch', latest_email_uid, '(RFC822)')
    email_message = email.message_from_bytes(email_data[0][1])
    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = email_message['From']
    email_to = email_message['To']
    subject = email_message['Subject']
    print(email_from + ' - '  + local_message_date)
    print (subject)
    print (get_body(email_message))

    
#latest_email_uid = data[0].split()[-1]
#result,data = connection.uid ('fetch',latest_email_uid,'(RFC822)')
#print(data[0][1])
#raw = email.message_from_bytes(data[0][1])
#print (raw['From'])
#print (raw['Subject'])
#print(get_body(raw))
#print(data[0])
connection.logout()

