from typing import Dict
from datetime import datetime
from flask import request
import hashlib
import yagmail
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD


def parse_data(request: request):
    localities: Dict[str, str] = {'001': 'Accomack County',
                                  '003': 'Albemarle County',
                                  '510': 'Alexandria City',
                                  '005': 'Alleghany County',
                                  '007': 'Amelia County',
                                  '009': 'Amherst County',
                                  '011': 'Appomattox County',
                                  '013': 'Arlington County',
                                  '015': 'Augusta County',
                                  '017': 'Bath County',
                                  '019': 'Bedford County',
                                  '021': 'Bland County',
                                  '023': 'Botetourt County',
                                  '520': 'Bristol City',
                                  '025': 'Brunswick County',
                                  '027': 'Buchanan County',
                                  '029': 'Buckingham County',
                                  '530': 'Buena Vista City',
                                  '031': 'Campbell County',
                                  '033': 'Caroline County',
                                  '035': 'Carroll County',
                                  '036': 'Charles City County',
                                  '037': 'Charlotte County',
                                  '540': 'Charlottesville City',
                                  '550': 'Chesapeake City',
                                  '041': 'Chesterfield County',
                                  '053': 'Clarke County',
                                  '570': 'Colonial Heights City',
                                  '580': 'Covington City',
                                  '045': 'Craig County',
                                  '047': 'Culpeper County',
                                  '049': 'Cumberland County',
                                  '590': 'Danville City',
                                  '051': 'Dickenson County',
                                  '053': 'Dinwiddie County',
                                  '595': 'Emporia City',
                                  '057': 'Essex County',
                                  '600': 'Fairfax City',
                                  '059': 'Fairfax County',
                                  '610': 'Falls Church City',
                                  '061': 'Fauquier County',
                                  '063': 'Floyd County',
                                  '065': 'Fluvanna County',
                                  '620': 'Franklin City',
                                  '067': 'Franklin County',
                                  '069': 'Frederick County',
                                  '630': 'Fredericksburg City',
                                  '640': 'Galax City',
                                  '071': 'Giles County',
                                  '073': 'Gloucester County',
                                  '075': 'Goochland County',
                                  '077': 'Grayson County',
                                  '079': 'Greene County',
                                  '081': 'Greensville County',
                                  '083': 'Halifax County',
                                  '650': 'Hampton City',
                                  '085': 'Hanover County',
                                  '660': 'Harrisonburg City',
                                  '087': 'Henrico County',
                                  '089': 'Henry County',
                                  '091': 'Highland County',
                                  '670': 'Hopewell City',
                                  '093': 'Isle Of Wight County',
                                  '095': 'James City County',
                                  '097': 'King &amp; Queen County',
                                  '099': 'King George County',
                                  '101': 'King William County',
                                  '103': 'Lancaster County',
                                  '105': 'Lee County',
                                  '678': 'Lexington City',
                                  '107': 'Loudoun County',
                                  '109': 'Louisa County',
                                  '111': 'Lunenburg County',
                                  '680': 'Lynchburg City',
                                  '113': 'Madison County',
                                  '683': 'Manassas City',
                                  '685': 'Manassas Park City',
                                  '690': 'Martinsville City',
                                  '115': 'Mathews County',
                                  '117': 'Mecklenburg County',
                                  '119': 'Middlesex County',
                                  '121': 'Montgomery County',
                                  '125': 'Nelson County',
                                  '127': 'New Kent County',
                                  '700': 'Newport News City',
                                  '710': 'Norfolk City',
                                  '131': 'Northampton County',
                                  '133': 'Northumberland County',
                                  '720': 'Norton City',
                                  '135': 'Nottoway County',
                                  '137': 'Orange County',
                                  '139': 'Page County',
                                  '141': 'Patrick County',
                                  '730': 'Petersburg City',
                                  '143': 'Pittsylvania County',
                                  '735': 'Poquoson City',
                                  '740': 'Portsmouth City',
                                  '145': 'Powhatan County',
                                  '147': 'Prince Edward County',
                                  '149': 'Prince George County',
                                  '153': 'Prince William County',
                                  '155': 'Pulaski County',
                                  '750': 'Radford City',
                                  '157': 'Rappahannock County',
                                  '760': 'Richmond City',
                                  '159': 'Richmond County',
                                  '770': 'Roanoke City',
                                  '161': 'Roanoke County',
                                  '163': 'Rockbridge County',
                                  '165': 'Rockingham County',
                                  '167': 'Russell County',
                                  '775': 'Salem City',
                                  '169': 'Scott County',
                                  '171': 'Shenandoah County',
                                  '173': 'Smyth County',
                                  '175': 'Southampton County',
                                  '177': 'Spotsylvania County',
                                  '179': 'Stafford County',
                                  '790': 'Staunton City',
                                  '800': 'Suffolk City',
                                  '181': 'Surry County',
                                  '183': 'Sussex County',
                                  '185': 'Tazewell County',
                                  '810': 'Virginia Beach City',
                                  '187': 'Warren County',
                                  '191': 'Washington County',
                                  '820': 'Waynesboro City',
                                  '193': 'Westmoreland County',
                                  '830': 'Williamsburg City',
                                  '840': 'Winchester City',
                                  '195': 'Wise County',
                                  '197': 'Wythe County',
                                  '199': 'York County'}

    reasons: Dict[str, str] = {
        '1A': 'Student attending college or university outside of locality of residence in Virginia',
        '1B': 'Spouse of student attending college or university outside locality of residence in Virginia',
        '1C': 'Business outside County/City of residence on election day',
        '1D': 'Personal business or vacation outside County/City of residence on election day',
        '1E': 'I am working and commuting to/from home for 11 or more hours between 6:00 AM and 7:00 PM on election day',
        '1F': 'I am a first responder (member of law enforcement, fire fighter, emergency technician, search and rescue)',
        '2A': 'My disability or illness',
        '2B': 'I am primarily and personally responsible for the care of a disabled/ill family member confined at home',
        '2C': 'My pregnancy',
        '3A': 'Confined, awaiting trial',
        '3B': 'Confined, convicted of a misdemeanor',
        '4A': 'An electoral board member, registrar, officer of election, or custodian of voting equipment',
        '5A': 'I have a religious obligation',
        '6A': 'Active Duty Merchant Marine or Armed Forces',
        '6B': 'Spouse or dependent living with a member of the Armed Forces or Active Duty Merchant Marine',
        '6C': 'Temporarily residing outside of US',
        '6D': 'Temporarily residing outside of US for employment or spouse or dependent residing with employee',
        '7A': 'Requesting a ballot for presidential and vice-presidential electors only (Ballots for other offices/issues will not be sent)',
        '8A': 'Authorized representative of candidate or party serving inside the polling place'
    }

    absentee_first_name: str = request.form['name__first']
    absentee_middle_name: str = request.form['name__middle']
    absentee_last_name: str = request.form['name__last']
    absentee_suffix: str = request.form['name__suffix']
    absentee_ssn: str = request.form['name__ssn']

    election_type: str = request.form['election__type']
    election_date: str = datetime.strftime(datetime.strptime(
        request.form['election__date'], '%d-%m-%y'), '%m %d %y')
    election_locality: str = localities[request.form['election__locality_gnis']]

    absentee_reason: str = reasons[request.form['reason__code']]
    absentee_reason_documentation: str = request.form['reason__documentation']

    absentee_birth_year: str = datetime.strftime(datetime.strptime(
        request.form.get('more_info__birth_year'), '%y'), '%y')
    absentee_telephone: str = request.form.get('more_info__telephone').replace(
        '-', '').replace('(', '').replace(')', '').replace(' ', '')
    absentee_telephone: str = absentee_telephone[:3] + ' ' + \
        absentee_telephone[3:-4] + ' ' + absentee_telephone[-4:]
    absentee_email: str = request.form.get('more_info__email_fax')

    absentee_street_address = request.form['address__street']
    absentee_unit = request.form['address__unit']
    absentee_city = request.form['address__city']
    absentee_state = request.form['address__state']
    absentee_zip = request.form['address__zip']

    delivery_destination = request.form.get('delivery__to')
    delivery_street_address = request.form.get('delivery__street')
    delivery_unit = request.form.get('delivery__unit')
    delivery_city = request.form.get('delivery__city')
    delivery_country = request.form.get('country')
    delivery_state = request.form.get('deliv-state')
    delivery_zip: str = request.form.get('delivery__zip').replace('-', '')
    # delivery_state_country = request.form.get('delivery__state_or_country')

    absentee_former_name = request.form.get('change__former_name')
    absentee_former_address = request.form.get('change__former_address')
    absentee_date_moved = (datetime.strftime(datetime.strptime(request.form.get(
        'change__date_moved'), '%d-%m-%y'), '%m %d %y')
        if request.form.get('change__date_moved') else "")
    absentee_assistance = request.form.get('assistance__assistance')

    assistant_signed = request.form.get('assistant__signed')
    assistant_name = request.form.get('assistant__name')
    assistant_street_address = request.form.get('assistant__street')
    assistant_unit = request.form.get('assistant__unit')
    assistant_city = request.form.get('assistant__city')
    assistant_state = request.form.get('assistant__state')
    assistant_zip = request.form.get('assistant__zip')
    assistant_signature = request.form.get('assistant__sig')

    absentee_agreement = request.form['checkbox']
    absentee_signature_date: str = datetime.strftime(datetime.strptime(
        request.form['signature__date'], '%d-%m-%y'), '%m %d %y')
    absentee_signature = request.form['signature__signed']

    data: Dict[str, str] = {
        "absentee_first_name": absentee_first_name,
        "absentee_middle_name": absentee_middle_name,
        "absentee_last_name": absentee_last_name,
        "absentee_suffix": absentee_suffix,
        "absentee_ssn": absentee_ssn,
        "election_type": election_type,
        "election_date": election_date,
        "election_locality": election_locality,
        "absentee_reason": absentee_reason,
        "absentee_reason_documentation": absentee_reason_documentation,
        "absentee_birth_year": absentee_birth_year,
        "absentee_telephone": absentee_telephone,
        "absentee_email": absentee_email,
        "absentee_street_address": absentee_street_address,
        "absentee_unit": absentee_unit,
        "absentee_city": absentee_city,
        "absentee_state": absentee_state,
        "absentee_zip": absentee_zip,
        # "delivery_state_country": delivery_state_country,
        "delivery_destination": delivery_destination,
        "delivery_street_address": delivery_street_address,
        "delivery_unit": delivery_unit,
        "delivery_city": delivery_city,
        "delivery_country": delivery_country,
        "delivery_state": delivery_state,
        "delivery_zip": delivery_zip,
        "absentee_former_name": absentee_former_name,
        "absentee_former_address": absentee_former_address,
        "absentee_date_moved": absentee_date_moved,
        "absentee_assistance": absentee_assistance,
        "assistant_signed": assistant_signed,
        "assistant_name": assistant_name,
        "assistant_street_address": assistant_street_address,
        "assistant_unit": assistant_unit,
        "assistant_city": assistant_city,
        "assistant_state": assistant_state,
        "assistant_zip": assistant_zip,
        "assistant_signature": assistant_signature,
        "absentee_agreement": absentee_agreement,
        "absentee_signature_date": absentee_signature_date,
        "absentee_signature": absentee_signature
    }
    print(data)
    return data


def build_pdf(data: Dict[str, str]):
    id: str = hashlib.md5(data).hexdigest()[:10]
    return id


def email_registrar(id: str):
    yagmail.SMTP(GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD).send(
        'registrar\'s email', 'subject', ['message', f'applications/{id}.pdf'])
