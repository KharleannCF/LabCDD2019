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
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

    # Body details
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            file_name = "email_" + str(x) + ".txt"
            output_file = open(file_name, 'w')
            output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, body.decode('utf-8')))
            output_file.close()
        else:
            continue
    print(email_from)
    print (subject)
    print (body)

    
#latest_email_uid = data[0].split()[-1]
#result,data = connection.uid ('fetch',latest_email_uid,'(RFC822)')
#print(data[0][1])
#raw = email.message_from_bytes(data[0][1])
#print (raw['From'])
#print (raw['Subject'])
#print(get_body(raw))
#print(data[0])
connection.logout()

