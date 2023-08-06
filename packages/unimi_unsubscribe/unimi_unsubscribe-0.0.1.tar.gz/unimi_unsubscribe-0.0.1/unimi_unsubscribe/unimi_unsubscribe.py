import json
import os
from pprint import pprint
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from time import sleep


def unsubscribe(user: str, password: str, server: str="smtp.unimi.it", sympa_mail: str="sympa@liste.unimi.it", port: int=465):
    """Method to unsubscribe from given sympa service.
        user: str, Your user name in the server, usually follows a format such as name.surname@studenti.unimi.it
        password: str, Your account password. We use SSL.
        server: str="smtp.unimi.it", Your SSL SMTP server account
        sympa_mail: str="sympa@liste.unimi.it", The address to which to send the unsubscribe mails.
        port: int=465, The SSL server port
    """
    server_ssl = SMTP_SSL(server, port)
    server_ssl.login(user, password)
    spam_path = "{dir}/spam_list.json".format(
        dir=os.path.dirname(os.path.realpath(__file__))
    )
    with open(spam_path, "r", encoding='utf-8') as f:
        spam_lists = json.load(f)
    print("Proceeding to unsubscribe from the following lists:")
    pprint(spam_lists)
    print("")
    print("Remember that you can always resubscribe to these.\n")
    sure = input("Proceed? [y/n] ")
    print("")
    if sure != "y":
        print("Entered {sure}, aborting.".format(sure=sure))
        return
    msg = MIMEText("\n".join(
        ["unsubscribe {spam}".format(spam=spam.split("@")[0]) for spam in spam_lists]), _charset="UTF-8")
    msg["Subject"] = ""
    msg["To"] = sympa_mail
    msg["From"] = user
    server_ssl.sendmail(user, sympa_mail, msg.as_string())
    server_ssl.close()
    print("All done: you will now receive a mail from the SYMPA service with the results of the unsubscribe commands.")
    print("Some lists cannot be unsubscribed with this channel, as they are required by the university.")
    print("You may receive an error from those lists.")
