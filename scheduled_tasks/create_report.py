from datetime import date
import openpyxl
import os

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def create_report() -> str:
    """ Call this daily at 5 am somehow, then save the filename for the day.
    It is not needed to save because it is just {thedate}.xls basically. """

    today_date: str = date.today().strftime("%m-%d-%y")

    report: openpyxl.workbook.Workbook = openpyxl.Workbook()
    sh: openpyxl.worksheet.worksheet.Worksheet = report.active
    sh['A1'] = 'Applicant Name'
    sh['B1'] = 'Time Submitted'
    sh['C1'] = 'SSN'
    sh['D1'] = 'Reason Code'
    sh['E1'] = 'Supporting Information'
    sh['F1'] = 'Registered to Vote Where'
    sh['G1'] = 'Email'
    sh['H1'] = 'Telephone Number'
    sh['I1'] = 'Address'
    sh['J1'] = 'IP Submitted From'
    sh['K1'] = 'Form ID'
    sh['L1'] = 'Canvasser ID'

    report_path: str = f'../reports/{today_date}.xlsx'

    report.save(report_path)
    return report_path


create_report()
