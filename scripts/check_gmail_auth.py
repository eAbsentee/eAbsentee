from dotenv import load_dotenv
load_dotenv()

from os import getenv
from yagmail import SMTP, logging as yag_logging
yag = SMTP(user=getenv("GMAIL_SENDER_ADDRESS"), password=getenv("GMAIL_SENDER_PASSWORD"))
yag.set_logging(yag_logging.DEBUG)
try:
    yag.login()
except:
    raise
else:
    print("authentication successful")
finally:
    yag.close()
