import requests
import smtplib

def get_emails():
    emails = {}

    try:
        email_file = open('emails.txt', 'r')

        for line in email_file:
            (email, name) = line.split(',')
            emails[email] = name.strip()
            
    except FileNotFoundError as err:
        print(err)
        
    return emails

def get_weather_forecast():
    url = 'http://api.apixu.com/v1/current.json?key=2ad97e687d664bb5ba520448163006&q=35.227085,-80.843124'
    weather_request = requests.get(url)
    weather_json = weather_request.json()
    weather_condition = weather_json['current']['condition']['text']
    weather_temp_c = weather_json['current']['temp_c']
    weather_temp_f = weather_json['current']['temp_f']

    forecast = 'Charlotte forecast for today is '
    forecast += weather_condition + 'with temperature of '
    forecast += str(int(weather_temp_c)) + 'C and ' + str(int(weather_temp_f)) + 'F!'
    return forecast

def send_emails(emails, forecast):
    # Connect to the smtp server
    server = smtplib.SMTP('smtp.gmail.com', '587')

    # Start TLS encryption
    server.starttls()

    # Login
    from_email = input("What's your email?")
    password = input("What's your password?")
    personal_msg = input("What message you want to send?")
    server.login(from_email, password)

    #Send to entire email list
    for to_email,name in emails.items():
        message = 'Subject: Python emailer! \n'
        message += 'Hi ' + name + '!\n\n'
        message += forecast + '\n\n' + personal_msg + '\n\n'
        server.sendmail(from_email, to_email, message)
    server.quit()
    
def main():
    emails = get_emails()
    print(emails)

    forecast = get_weather_forecast()
    print(forecast)

    send_emails(emails, forecast)
main()
