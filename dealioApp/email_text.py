import smtplib


def send_promo_text(number, title, description):
    tmobile = '@tmomail.net'
    verizon = '@vtext.com'
    sprint = '@messaging.sprintpcs.com'
    ATT = 'number@txt.att.net'

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    content = '-' + title + '\n' + description
    dealio = 'best.dealio.app@gmail.com'
    mail.login(dealio, '^B7GiF$IB2r8dct')
    mail.sendmail(dealio, number + tmobile, 'Subject: {}\n\n{}'.format('dealio', content))
    mail.sendmail(dealio, number + verizon, 'Subject: {}\n\n{}'.format('dealio', content))
    mail.sendmail(dealio, number + sprint, 'Subject: {}\n\n{}'.format('dealio', content))
    mail.sendmail(dealio, number + ATT, 'Subject: {}\n\n{}'.format('dealio', content))
    mail.close()


def send_promo_email(email, title, description):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    content = '-' + title + '\n' + description
    dealio = 'best.dealio.app@gmail.com'
    mail.login(dealio, '^B7GiF$IB2r8dct')
    mail.sendmail(dealio, email, 'Subject: {}\n\n{}'.format('dealio', content))
    mail.close()
