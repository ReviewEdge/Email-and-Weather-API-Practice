import smtplib
import imapclient
import imaplib
imaplib._MAXLINE = 10000000
import pprint
import pyzmail
import requests

last_message = ["null"]

def sendemail_input():
    # starts connection
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    # creates variables
    email = input("Enter your email adress: ")
    password = input("Enter password: ")
    sendaddress = input("Enter the recipient's email address: ")
    subject = input("Enter the email's subject: ")
    message = input("Enter the email's message: ")
    full_message = "Subject: " + subject + " " + " \n" + message
    # sends email
    smtpObj.login(email, password)
    smtpObj.sendmail(email, sendaddress, full_message)
    # quits connection
    smtpObj.quit()

def sendemail(email,password,sendaddress,subject,message):
    # starts connection
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    # creates variables
    full_message = "Subject: " + subject + " " + " \n" + message
    # sends email
    smtpObj.login(email, password)
    smtpObj.sendmail(email, sendaddress, full_message)
    # quits connection
    smtpObj.quit()


#forwards email from swimm to reviewedge
def email_forward():
    imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imapObj.login("swimmingonanarwhal@gmail.com", "2belugas")
    imapObj.select_folder("INBOX", readonly=False)

    while True:


        UIDs = imapObj.gmail_search("test1")
        # print(UIDs)
        rawMessages = imapObj.fetch(UIDs, ["BODY[]"])
        # pprint.pprint(rawMessages)
        # print(rawMessages.keys())
        message = pyzmail.PyzMessage.factory(rawMessages[UIDs[len(UIDs) - 1]][b'BODY[]'])
        # print(message)
        # print(rawMessages[7156].keys())
        if message.text_part != None:
            mes_use_text = message.text_part.get_payload().decode(str(message.text_part.charset))
        if message.html_part != None:
            mes_use_html = message.html_part.get_payload().decode(message.html_part.charset)

        stop_command = "stopnow"

        if stop_command in mes_use_text:
            print("Received shut down command. Shutting Down...")
            # for some reason the email this sends breaks the program:
            #sendemail("swimmingonanarwhal@gmail.com", "2belugas", "swimmingonanarwhal@gmail.com", "test1",
            #         "Email Forwarder has been shut down.")
            break

        if mes_use_text != last_message[len(last_message)-1]:
            print(mes_use_text)
            sendemail("swimmingonanarwhal@gmail.com","2belugas","reviewedge56@gmail.com",mes_use_text[:37],mes_use_text)
            last_message.append(mes_use_text)


# sends certain email after recieving email with certain subject, uses "stopnow" as stop command, uses swimmingonanarwhal email account
# ISSUES: doesn't work if email with key_sub hasn't been sent yet
def sendback_email(key_sub,recip_address,subject,message1):
    imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imapObj.login("swimmingonanarwhal@gmail.com", "2belugas")
    imapObj.select_folder("INBOX", readonly=False)

    while True:


        UIDs = imapObj.gmail_search(key_sub)
        # print(UIDs)
        rawMessages = imapObj.fetch(UIDs, ["BODY[]"])
        # pprint.pprint(rawMessages)
        # print(rawMessages.keys())
        message = pyzmail.PyzMessage.factory(rawMessages[UIDs[len(UIDs) - 1]][b'BODY[]'])
        # print(message)
        # print(rawMessages[7156].keys())
        if message.text_part != None:
            mes_use_text = message.text_part.get_payload().decode(message.text_part.charset)
        if message.html_part != None:
            mes_use_html = message.html_part.get_payload().decode(message.html_part.charset)

        stop_command = "stopnow"

        if stop_command in mes_use_text:
            print("Received shut down command. Shutting Down...")
            # for some reason the email this sends breaks the program:
            # sendemail("swimmingonanarwhal@gmail.com", "2belugas", "swimmingonanarwhal@gmail.com", key_sub,
            #
            break

        if mes_use_text != last_message[len(last_message)-1]:
            print(mes_use_text)
            sendemail("swimmingonanarwhal@gmail.com","2belugas",recip_address,subject,message1)
            last_message.append(mes_use_text)


#used as modifier: calculator
def calc(input_mes):
    use_mes = input_mes[5:]
    ans = str(use_mes) + "= " + str(eval(use_mes))
    return ans

#used as modifier: weather -sends weather for Jamestown, NY
def weather1(input_mes):
    city_id = "5122534"
    url = "http://api.openweathermap.org/data/2.5/weather?id=" + city_id + "&units=imperial&APPID=c3e072c5029f60ac53dac3d1c7d9b06f"
    json_data = requests.get(url).json()

    temp_val = str(json_data["main"]["temp"])
    temp_val = temp_val[:len(temp_val) - 3]

    description = str(json_data["weather"][0]["description"])
    description = description.capitalize()

    format_add = description + "\n" + "Temperature: " + temp_val + " " + "degrees F"
    return "Current weather in Jamesown, NY: \n\n" + format_add






#when it recieves an email with a key word, it will send back a certain message to a certain address -modifies with custom modifier function
#input modifier WITHOUT parenthesis
#ISSUES: gets messed up if subject has matching words with key_sub
#ISSUES: needs to access message being checked to send calculation, which means sendback_email needs to split into more individual functions (one part reads emails, onepart sends them
#ISSUES: needs to be able to check if email has calculation or not
#def email_calc():
    #sendback_email("calc","swimmingonanarwhal@gmail.com","Calculated Answer",calc(mes_use_text))

#doesn't need for "calc" at the beginning of the message
#opened version of email_calc:
#ISSUES: needs to be able to check if email has calculation or not
#ISSUES: TypeError: can only concatenate str (not "int") to str
#doesn't send again if it's the same message twice
#Try to make it decide to send or not based on time of recieving message
def email_response_sender(key_sub,recip_address,subject,modifier):
    imapObj = imapclient.IMAPClient("imap.gmail.com", ssl=True)
    imapObj.login("swimmingonanarwhal@gmail.com", "2belugas")
    imapObj.select_folder("INBOX", readonly=False)

    while True:


        UIDs = imapObj.gmail_search(key_sub)
        # print(UIDs)
        rawMessages = imapObj.fetch(UIDs, ["BODY[]"])
        # pprint.pprint(rawMessages)
        # print(rawMessages.keys())
        message = pyzmail.PyzMessage.factory(rawMessages[UIDs[len(UIDs) - 1]][b'BODY[]'])
        # print(message)
        # print(rawMessages[7156].keys())
        if message.text_part != None:
            mes_use_text = message.text_part.get_payload().decode(message.text_part.charset)
        #interperets html, doesn't get used yet
        if message.html_part != None:
            mes_use_html = message.html_part.get_payload().decode(message.html_part.charset)

        stop_command = "stopnow"

        if stop_command in (mes_use_text).lower():
            print("Received shut down command. Shutting Down...")
            # for some reason the email this sends breaks the program:
            # sendemail("swimmingonanarwhal@gmail.com", "2belugas", "swimmingonanarwhal@gmail.com", key_sub,
            #
            break

        if mes_use_text != last_message[len(last_message)-1]:
            print(mes_use_text)
            sendemail("swimmingonanarwhal@gmail.com","2belugas",recip_address,subject,modifier(mes_use_text))
            last_message.append(mes_use_text)
    sendemail("swimmingonanarwhal@gmail.com", "2belugas", recip_address, "Process Ended", "The program \"" + key_sub + "\" has been shut down.")







#Runs the email calculator using "calc" as keyword
#email_response_sender("calc","swimmingonanarwhal@gmail.com", "Calculated Answer",calc)

#runs the email weather using "weather" as keyword
#email_response_sender("weather","swimmingonanarwhal@gmail.com","Current Conditions",weather1)





#used as modifier: weather -sends weather for Jamestown, NY
def weather2(input_mes):
    city_id = "5122534"
    url = "http://api.openweathermap.org/data/2.5/weather?id=" + city_id + "&units=imperial&APPID=c3e072c5029f60ac53dac3d1c7d9b06f"
    json_data = requests.get(url).json()

    temp_val = str(json_data["main"]["temp"])

    #Removes decimal but sometimes messes up temp val and removes essential numbers:
    #temp_val = temp_val[:len(temp_val) - 3]

    description = str(json_data["weather"][0]["description"])
    description = description.capitalize()

    format_add = description + "\n" + "Temperature: " + temp_val + " " + "degrees F"
    return "Current weather in Jamesown, NY: \n\n" + format_add

print(weather2(1))

