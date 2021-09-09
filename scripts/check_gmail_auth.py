from dotenv import load_dotenv
load_dotenv()

from os import getenv
from yagmail import SMTP, logging as yag_logging
yag = SMTP(user=getenv("GMAIL_SENDER_ADDRESS"), password=getenv("GMAIL_SENDER_PASSWORD"))
yag.set_logging(yag_logging.DEBUG)
try:
    yag.login()
except:
    # raise
    from sys import stderr
    print("authentication failed", file=stderr)
    print("to fix the issue, try going to https://myaccount.google.com/lesssecureapps and enabling less secure app access")
else:
    print("authentication successful")
finally:
    yag.close()
