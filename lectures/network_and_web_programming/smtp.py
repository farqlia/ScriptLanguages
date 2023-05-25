import smtplib
import ssl

port = 587
smtp_server = "smtp.gmail.com"
sender_email = "email2@gmail.com"
receiver_email = "email2@gmail.com"
# Hasła do aplikacji -> można stworzyć hasło do aplikacji
password = ""

message = "Hello from the other side"

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
