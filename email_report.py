import yagmail
from datetime import date
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import os

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def email_report() -> None:
    """Email the Excel spreadsheet to Senator Surovell and Mr. Rouvelas. """
    today_date: str = date.today().strftime("%m-%d-%y")
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        to=['raunakdaga@gmail.com'],
        # to=['ssurovell@gmail.com', 'lerouvelas@gmail.com']
        subject=f'Daily Absentee Ballot Application Report - {today_date}',
        contents=f'Please find attached the daily report of absentee ' + \
        f'ballot applications for {today_date}.',
        attachments=f'reports/{today_date}.xlsx'
    )


email_report()
