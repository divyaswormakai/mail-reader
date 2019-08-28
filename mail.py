import smtplib
import time
import imaplib
import email
import re
import glob
import os
import getpass

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def readmail():
    filesPath = os.path.join("D:\\code problems\\",'*')
    files = sorted(glob.iglob(filesPath),key =os.path.getctime,reverse = True)
    latest_file = files[0]
    latest_file_num = re.findall(r'\d+',latest_file)
    latest_file_num = int(latest_file_num[0])
    print(str(latest_file_num)+"is the latest file")
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        FROM_EMAIL = input("Input email:")
        FROM_PWD = getpass.getpass()
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        type,data = mail.search(None,'(UNSEEN)')
        mail_ids = data[0]
        id_list = mail_ids.split()
        last_email = int(id_list[-1])
        first_email = int(id_list[0])
        print(first_email,last_email)
        
        print("Processing mails")
        for i in range(first_email,last_email+1):
            typ,datas = mail.fetch(str(i),'(RFC822)')
            for response in datas:
                if isinstance(response,tuple):
                        msg = email.message_from_bytes(response[1])
                        sub = msg["Subject"]
                        sender = msg["From"]
                        if(sender == "Daily Coding Problem <founders@dailycodingproblem.com>"):
                            numb = re.findall(r'\d+',sub)
                            if(msg.is_multipart()):
                                allpart = msg.get_payload();
                                part = allpart[0]
                                if(part.get_content_maintype() =='text'):
                                    body = part.get_payload().split("-------------------------------------------------------------=",1)
                                    # print(body[0])
                                    if(latest_file_num<int(numb[0])):
                                        file_name = "D:\\code problems\\"+numb[0]+".py"
                                        print(file_name)
                                        file = open(file_name, 'a')
                                        file.writelines(body[0])
                                        file.close()
                                        break
                                    else:
                                        break
                                        
    except Exception as e:
        print("Error:"+str(e))

    print("---completed----")

if __name__=="__main__":
    readmail()