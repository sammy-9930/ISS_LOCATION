import smtplib

import requests
from datetime import datetime

MY_LAT = 12.971599 # Your latitude
MY_LONG = 77.594566 # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


if is_iss_overhead() and is_night():
    email_address = input("Enter your email address: ")
    password = input("Enter your password")
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(email_address, password)
    connection.sendmail(
        from_addr=email_address,
        to_addrs=email_address,
        msg="Subject:Look Up\n\nThe ISS is above you in the sky."
    )
