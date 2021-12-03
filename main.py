import time
import os
import sys
from ga.GeneticAlgo import GeneticAlgo
from ga.data.reader import read_game_data, read_sf_data
from ga.data.output import bits_to_sched

# sending emails with attachments using SMTP requires building emails in mime format
import smtplib
import email
import email.mime.application
import email.mime.text
import email.mime.multipart

root = os.path.dirname(os.path.abspath(__file__))
big_folder = '/data/model'
tiny_folder = '/ga/data/test'

global days
global receiver
receiver = sys.argv[1]
sf_email = os.getenv('SF_EMAIL')
sf_pass = os.getenv('SF_PASS')

# send email
def send_email():
    """Shoot client with mailgun!"""
    global days
    attachmentpath = root + '/data/'

    # MIME format message
    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = 'Your generated schedules are in!'
    msg['From'] = sf_email
    msg['to'] = receiver

    # main body is an attachment
    body = email.mime.text.MIMEText('Greetings, \n'
                                    '    \n'
                                    'Attached are your generated schedules! We hope they are to your satisfaction.\n'
                                    '    \n'
                                    'Sincerely, \n'
                                    'The Automated SF Scheduler Team\n')
    msg.attach(body)

    # HTML attachment/s
    for i in range(0, days):
        filename = 'modelresult' + str(i) + '.html'
        fp = open(attachmentpath + filename, 'rb')
        att = email.mime.application.MIMEApplication(fp.read(), _subtype="html")
        fp.close()
        att.add_header('Content-Disposition', 'attachment', filename='Day ' + str(i+1) + '.html')
        msg.attach(att)

    try:
        s = smtplib.SMTP('smtp.mailgun.org', 587)
        s.login(sf_email, sf_pass)
        s.sendmail(sf_email, receiver, msg.as_string())
        s.quit()
        print('email successfully sent!')
    except smtplib.SMTPException:
        print('Error: unable to send email')


# test parameters
ga_params = {
    'selection_method': 'rank',
    'crossover_method': 'uniform',
    'mutation_method': 'bit_flip',
    'threshold': 10,
    'pop_size': 10,
    'mutation_rate': 0.1,
    'game_src': root + big_folder + '/big_game_data.csv',
    'sf_src': root + big_folder + '/big_sf_data.csv',
    'fitness_src': root + big_folder + '/big_fitness.csv',
    'crossover_params': {'children': 2, 'n_breaks': 5}
}


def all_cross_mut():
    for i in ['one_point', 'n_point', 'uniform']:
        ga_params['crossover_method'] = i
        for j in ['bit_flip', 'flip_all', 'uniform']:
            ga_params['mutation_method'] = j
            ga_params['fitness_src'] = (root + big_folder +
            '/cross_mut/fitness_' + i[0] + j[0] + '.csv')
            __main__()


def __main__():
    ga_obj = GeneticAlgo(**ga_params)

    t_start = time.perf_counter()
    best = ga_obj.ga()
    print(best)
    t_end = time.perf_counter()
    print(f"Time in seconds: {t_end-t_start:0.4f}")
    sf_data = read_sf_data(ga_params['sf_src'])
    game_data = read_game_data(ga_params['game_src'])
    df = bits_to_sched(best, sf_data, game_data)
    for i, day in enumerate(df):
        day.to_html(root + big_folder + 'result' + str(i) + '.html', escape=False)
        day.to_csv(root + big_folder + 'result' + str(i) + '.csv')
        global days
        days = i + 1
    print(df)
    print(days)


__main__()
send_email()

