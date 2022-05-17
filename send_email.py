import smtplib
import ssl


def send():
    port = 465
    smtp_server = 'thenakedscientists.co.za'
    sender_email = 'mbudzeni@thenakedscientists.co.za'
    receiver_email = 'mbudzenin@yahoo.com'
    password = 'thiVhafuni8'
    message = """\
    Subject: Hi,
    
    This message is sent from Python Script.
    """
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def main():
    send()


if __name__ == '__main__':
    main()
