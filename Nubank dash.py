import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import smtplib
#importando a senha do e-mail
from segredo import senha
#
import pathlib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase
from datetime import datetime, date


# criar tabela concatenada #
path = os.getcwd() +'/' + input('Insira o nome da sua pasta:')
e_mail = input('Insira seu E-mail:')
files = [file for file in os.listdir(path) if not file.startswith('.')]
all_months_df = pd.DataFrame()
for file in files:
    current_df = pd.read_csv(path + "/" + file)
    all_months_df = pd.concat([all_months_df, current_df])

all_months_df.to_csv("Gastos.csv", index=False)

# ler a tabela criada #
nu_df = pd.read_csv('Gastos.csv')

# Drop NaN #
nu_df = nu_df.dropna()

# correções #
nu_df['amount'] = pd.to_numeric(nu_df['amount'])
nu_df['month'] = pd.to_datetime(nu_df['date']).dt.month
nu_df['year'] = pd.to_datetime(nu_df['date']).dt.year

# vars para os plots#
gastos = nu_df.drop('year', axis = 1).groupby('month').sum()
print(gastos)
months = range(1,13)

meme = nu_df.groupby('category')
categ_totals = meme.sum()['amount']
print(categ_totals)
categ = [category for category, df in meme]

figure, axis = plt.subplots(1, 2)
axis[0].bar(months,gastos['amount'])
axis[0].set_title('Gastos Mensais')
axis[0].set_xticks(months)
axis[0].set_xlabel('Meses')
axis[0].set_ylabel('Gastos R$')
axis[1].bar(categ, categ_totals)
axis[1].set_title('Gastos por Categoria')
axis[1].set_xticklabels(categ, rotation = 'vertical', size = 8)
axis[1].set_xlabel('Categorias')
axis[1].set_ylabel('Gastos R$')
plt.tight_layout()
plt.savefig('Gastos.png', bbox_inches ='tight')
plt.savefig('Gastos.png', bbox_inches ='tight')
img_path = './Gastos.png'

# Settings
from_mail = "pendragonpc@gmail.com"
from_password = senha

to_mail = e_mail

smtp_server = "smtp.gmail.com"
smtp_port = 465


def send_email(path_plot, smtp_server, smtp_port, from_mail, from_password, to_mail):
    '''
        Send results via mail
    '''

    # Create the email message
    msg = MIMEMultipart()
    msg['Subject'] = 'Data Report Nubank'
    msg['From'] = from_mail
    COMMASPACE = ', '
    msg['To'] = COMMASPACE.join([from_mail, to_mail])
    msg.preamble = 'Data Report: Nubank'

    # Open the files in binary mode and attach to mail
    with open(img_path, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='graphs.png')
        img.add_header('X-Attachment-Id', '0')
        img.add_header('Content-ID', '<0>')
        fp.close()
        msg.attach(img)

    # Attach HTML body
    msg.attach(MIMEText(
        f'''
        <html>
            <body>
                <h1 style="text-align: center;">Report Faturas</h1>
                
                <p>Gastos Mensais:</p>
                {gastos.to_html(formatters={'Gastos por Mês': 'R${:,.2f}'.format})}
                <p>Report das suas faturas do Nubank.</p>
                <p><img src="cid:0"></p>
            </body>
        </html>'
        ''',
        'html', ' utf-8 '))

    # Send mail
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.ehlo()
    server.login(from_mail, from_password)

    server.sendmail(from_mail, [from_mail, to_mail], msg.as_string())
    server.quit()


send_email(img_path, smtp_server, smtp_port, from_mail, from_password, to_mail)



print('Email Enviado')





