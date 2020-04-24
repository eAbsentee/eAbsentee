# eAbsentee: Absentee Ballot Request System

A web app built with Flask which allows users to submit applications for absentee ballots in the state of Virginia. Somebody who wants an absentee ballot can complete a web form, and eAbsentee will use their input to complete the state-sanctioned PDF and email it to the state registrar of their locality. eAbsentee is based off of and expands upon [Horatio](https://github.com/TrustTheVote-Project/horatio-client), the original online absentee ballot application.

Absentee ballot request forms may be submitted electronically in Virginia under the authority of [attorney general opinion #13-111](http://ag.virginia.gov/files/Opinions/2014/13-111_Hinshaw.pdf) and [approval of the State Board of Elections](https://townhall.virginia.gov/L/GetFile.cfm?File=meeting\151\22788\Minutes_SBE_22788_v2.pdf). (p. 7, lines 189–215).

### How it Works

-   Creates JSON object from user input data
-   Uses `pdfrw` to populate a PDF template using Cartesian coordinates
-   Sends the PDF to the state registrar of the appropriate locality
-   If the email bounces, it's sent to a catch email, where we then forward it to the appropriate registrar
-   Tracks data for reporting to groups

## Development

-   Create a file called `keys.py` with the following format:

```python
GMAIL_SENDER_ADDRESS = 'applications@eAbsentee.org'
GMAIL_SENDER_PASSWORD = '<PASSWORD>'
SECRET_KEY = '<SECRET KEY>'
API_KEY = '<API KEY>'
```
-   Create `static/credentials.json` and `static/storage.json` with the correct content, which are both for the Google API

-   Run `pipenv install`

-   Run `pipenv shell`

-   Run `python scheduled_tasks/email_bounceback.py`, and login to your GMAIL-enabled API account.

-   Run `export FLASK_ENV=development`

-   Run `flask run`

## Campaigns and Groups

A campaign in eAbsentee is a link which leads to a form which only contains a designated set of counties. For example, if a user
heads to eAbsentee.org/campaign/surovell, when they click on the form, they won't see all 95 Virginia counties, but rather only
those that the Surovell campaign has elected to display.

A group in eAbsentee is a link that is simply used to track where users come from. Once a user clicks on a group link, which are normally structured like eAbsentee.org/group/surovell, their group code is set in their cookies. This only matters when a user fills
out the ballot request form, at which point data will be logged about which group they came from.

## Contact

-   If you have questions, please email raunak@eAbsentee.org
