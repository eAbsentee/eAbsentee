#!/usr/bin/env python
# Jacob Salmela
# 2016-06-02
# Writes text to a PDF at coordinates.  Use for quickly filling out forms that you use regularly.
# This takes some manual setup, but saves a ton of time once done

# http://stackoverflow.com/a/17538003
# Make sure to install the two utilities below first
# sudo easy_install pypdf2
# sudo easy_install reportlab

import sys
import os
import io
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get the filename and extension so we can use it for renaming the newly-created file
filename, file_extension = 'static/blankApp', '.pdf'

# Append "-filled" to the filename and save it in the same place
# This retains the original file so it can be used again with the script
# It also saves the file in the same folder so it's easy to find
filled_out_file = filename + "-filled" + file_extension

# Re-use for any checkboxes
checkbox = "X"

# Information for the form
# Varibles and their names can be changed to anything depending on the form being filled out
# Date of service and date needed by can be a second argument since the rest of the information will stay pretty much the same
patient_name = "My Dude"
patient_dob = "01/01/1970"
hospital_name = "Sickbay"
hospital_address = "X"
hospital_phone = "123.456.7890"
release_to = "Jacob Salmela"
phone_number = "123.456.7890"
address = "Deck 10, Enterprise D"
date_signed = time.strftime("%d/%m/%Y")


def main():
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    # This would do better in a loop using some key/value pairs, but this is good enough for government work
    can.drawString(180, 690, patient_name)  # LastName
    can.drawString(420, 690, patient_dob)  # First Name
    can.drawString(185, 666, hospital_name)  # Middle Name
    can.drawString(320, 666, hospital_name)  # Suffix
    can.drawString(238, 638, hospital_address)  # Gen/Spec Election
    can.drawString(383, 638, hospital_address)  # Democratic Primary
    can.drawString(498, 638, hospital_address)  # Republican Primary
    can.drawString(550, 675, '2  3  1  4')  # SSN
    can.drawString(207, 614, '1   1')  # MonthOfElection
    can.drawString(251, 614, "1   1")  # Dayofelection
    can.drawString(291, 614, "1   1")  # YearOfElection

    can.drawString(331, 611, "X")  # REGISTERED COUNTY
    can.drawString(378, 611, "X")  # REGISTERED CITY
    can.drawString(425, 611, 'This is the locality')  # Registered locality

    can.drawString(189, 554, 'A     4')
    can.drawString(312, 555, 'Supporting Information')

    can.drawString(183, 522, '1   9   9   0')  # Birth Year
    can.drawString(423, 524, '7   0   0')  # FIRST 3 TELPEHONE
    can.drawString(480, 524, '7   0   0')  # SECOND 3 TELPEHONE
    can.drawString(537, 524, '7   0   0   4')  # LAST 4 TELPEHONE
    can.drawString(178, 504, 'Email/fax')

    can.drawString(171, 473, 'Residence Address')
    can.drawString(516, 473, 'APT/SUITE')
    can.drawString(153, 453, 'cITY')
    can.drawString(518, 453, '5   5   5   5   5')  # ZIP CODE OF DELIVERY

    can.drawString(289, 424, checkbox)  # DELIVERED TO RESIDENCE
    can.drawString(459, 424, checkbox)  # DELIVERED TO MAILING
    can.drawString(289, 410, checkbox)  # DELIVERED TO EMAIL
    can.drawString(459, 410, checkbox)  # DELIVERED TO FAX
    can.drawString(168, 392, 'MailingAddress')
    can.drawString(532, 392, 'Mailing Apt')
    can.drawString(154, 372, 'Mailing City')
    can.drawString(317, 372, 'STATE/COUNTRY')
    can.drawString(442, 372, '5   5   5   5   5')

    can.drawString(205, 340, 'Former Full Name')
    can.drawString(487, 340, '0   0')  # MONTH MOVED
    can.drawString(528, 340, '0   0')  # DAY MOVED
    can.drawString(569, 340, '0   0')  # YEAR MOVED
    can.drawString(192, 320, 'Former Address')

    can.drawString(247, 103, 'Signature')
    can.drawString(492, 103, '0   0')  # Date Signed
    can.drawString(529, 103, '0   0')  # Month Signed
    can.drawString(529, 103, '0   0')  # Month Signed
    # Apply the changes
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # Read the existing PDF (the first argument passed to this script)
    existing_pdf = PdfFileReader(filename + file_extension, "rb")
    output = PdfFileWriter()

    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # Finally, write "output" to a real file
    output.write(open(filled_out_file, "wb"))


if __name__ == "__main__":
    main()
