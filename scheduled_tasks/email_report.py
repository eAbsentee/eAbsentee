import yagmail
from datetime import date
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD
import os
import openpyxl
from openpyxl import load_workbook

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('../reports/dailyreports')


def split_reports() -> None:
    pass


def email_report() -> None:
    print(os.path.dirname(os.path.realpath(__file__)))
    """Email the Excel spreadsheet to Senator Surovell and Mr. Rouvelas. """
    today_date: str = date.today().strftime("%m-%d-%y")
    report_path = f'{today_date}.xlsx'
    report: openpyxl.workbook.Workbook = load_workbook(filename=report_path)
    worksheet: openpyxl.worksheet.worksheet.Worksheet = report.active
    if worksheet['A2'].value:
        yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
            to=['raunakdaga@gmail.com', 'ssurovell@gmail.com', 'lerouvelas@gmail.com'],
            # to=['ssurovell@gmail.com', 'lerouvelas@gmail.com'],
            # to='raunakdaga@gmail.com',
            subject=f'Daily Absentee Ballot Application Report - {today_date}',
            contents=f'Please find attached the daily report of absentee ' + \
            f'ballot applications for {today_date}.',
            attachments=report_path
        )


email_report()
