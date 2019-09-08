import os
import io
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


def main():
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(180, 690, lastName)  # LastName
    can.drawString(420, 690, firstName)  # First Name
    can.drawString(185, 666, middleName)  # Middle Name
    can.drawString(320, 666, suffix)  # Suffix
    can.drawString(238, 638, genSpecCheck)  # Gen/Spec Election
    can.drawString(383, 638, demPrimCheck)  # Democratic Primary
    can.drawString(498, 638, repPrimCheck)  # Republican Primary
    can.drawString(550, 675, ssn)  # SSN
    can.drawString(207, 614, dateOfElectionMonth)  # MonthOfElection
    can.drawString(251, 614, dateOfElectionDay)  # Dayofelection
    can.drawString(291, 614, dateOfElectionYear)  # YearOfElection

    can.drawString(331, 611, countyCheck)  # REGISTERED COUNTY
    can.drawString(378, 611, cityCheck)  # REGISTERED CITY
    can.drawString(425, 611, registeredToVote)  # Registered locality

    can.drawString(189, 554, reasonCode)
    can.drawString(312, 555, supporting)

    can.drawString(183, 522, birthYear)  # Birth Year
    can.drawString(423, 524, firstThreeTelephone)  # FIRST 3 TELPEHONE
    can.drawString(480, 524, secondThreeTelephone)  # SECOND 3 TELPEHONE
    can.drawString(537, 524, lastFourTelephone)  # LAST 4 TELPEHONE
    can.drawString(178, 504, email)

    can.drawString(171, 473, address)
    can.drawString(516, 473, apt)
    can.drawString(153, 453, city)
    can.drawString(518, 453, zipCode)  # ZIP CODE OF DELIVERY

    can.drawString(289, 424, deliverResidence)  # DELIVERED TO RESIDENCE
    can.drawString(459, 424, deliverMailing)  # DELIVERED TO MAILING
    can.drawString(289, 410, deliverEmail)  # DELIVERED TO EMAIL
    # can.drawString(459, 410, deliverFax)  # DELIVERED TO FAX
    can.drawString(168, 392, ballotDeliveryAddress)
    can.drawString(532, 392, ballotDeliveryApt)
    can.drawString(154, 372, ballotDeliveryCity)
    can.drawString(317, 372, ballotDeliveryState)
    can.drawString(442, 372, ballotDeliveryZip)

    can.drawString(205, 340, formerFullName)
    can.drawString(487, 340, dateMovedMonth)  # MONTH MOVED
    can.drawString(528, 340, dateMovedDay)  # DAY MOVED
    can.drawString(569, 340, dateMovedYear)  # YEAR MOVED
    can.drawString(192, 320, formerAddress)

    can.drawString(130, 292, assistantCheck)  # Assistant checkbox
    can.drawString(170, 222, assistantFullName)
    can.drawString(165, 202, assistantAddress)
    can.drawString(513, 202, assistantApt)
    can.drawString(150, 182, assistantCity)
    can.drawString(363, 182, assistantState)
    can.drawString(517, 182, assistantZip)
    can.drawString(170, 162, assistantSignature)

    can.drawString(247, 103, signature)
    can.drawString(492, 103, todaysDateMonth)  # Month Signed
    can.drawString(529, 103, todaysDateDay)  # Day Signed
    can.drawString(569, 103, todaysDateYear)  # Year Signed

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
