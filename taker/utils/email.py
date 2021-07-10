import ssl
import smtplib
import threading
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(quiz, taker):
    print("Sending mail")
    port = 465
    password = "You can't cracky m3!"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        sender_email = "fordblogging@gmail.com"
        server.login(sender_email, password)
        # receiver_email = "dummyani26@gmail.com"
        receiver_email = taker.email

        msg = MIMEMultipart('alternative')

        text = f'Check out the correct answers to the quiz - {quiz.name}'

        html = f"""\
                <html>
                  <head></head>
                  <body>
                    <p>
                       Check out the correct answers to the quiz - {quiz.name} <br>
                       Here is the <a href='https://ani-quiz-maker.herokuapp.com/take-quiz/{quiz.id}/{taker.id}/result/'>link</a>.
                    </p>
                  </body>
                </html>
                """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        msg['Subject'] = 'Pro Quiz'
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server.send_message(msg)
        server.quit()


def setSendEmailTimer(quiz, taker, interval):
    timer = threading.Timer(interval, sendEmail, args=[quiz, taker])
    timer.start()
