from datetime import date
from Flask import request
import localities_info


def parse_data(request: request):
    today = date.today()
    todayDate = today.strftime("%m%d%y")

    absentee_telephone: str = request.form.get('more_info__telephone').replace(
        '-', '').replace('(', '').replace(')', '').replace(' ', '')

    data_dict = {
        'firstName': request.form['name__first'],
        'middleName': request.form['name__middle'],
        'lastName': request.form['name__last'],
        'suffix': request.form['name__suffix'],
        'ssn': request.form['name__ssn'],
        'reasonCode': request.form['reason__code'],
        'registeredToVote': localities_info.localities[
            request.form['election__locality_gnis']
        ]['locality'],
        'supporting': request.form['reason__documentation'],
        'birthYear': request.form.get('more_info__birth_year'),
        'email': request.form.get('more_info__email_fax'),
        'address': request.form['address__street'],
        'apt': request.form['address__unit'],
        'city': request.form['address__city'],
        'zipCode': request.form['address__zip'],
        'ballotDeliveryAddress': request.form.get('delivery__street'),
        'ballotDeliveryCity': request.form.get('delivery__city'),
        'ballotDeliveryApt': request.form.get('delivery__unit'),
        'ballotDeliveryZip': request.form.get('delivery__zip').replace('-', ''),
        'ballotDeliveryState': request.form.get('deliv-state'),
        'formerFullName': request.form.get('change__former_name'),
        'formerAddress': request.form.get('change__former_address'),
        'signature': request.form['signature__signed'],
        'firstThreeTelephone': absentee_telephone[0:3],
        'secondThreeTelephone': absentee_telephone[3:6],
        'lastFourTelephone': absentee_telephone[6:10],
        'assistantCheck': 'X' if request.form.get('assistance__assistance') == 'true' else '',
        'assistantFullName': request.form.get('assistant__name'),
        'assistantAddress': request.form.get('assistant__street'),
        'assistantSignature': request.form.get('assistant__signed'),
        'assistantApt': request.form.get('assistant__unit'),
        'assistantCity': request.form.get('assistant__city'),
        'assistantState': request.form.get('assistant__state'),
        'assistantZip': request.form.get('assistant__zip').replace('-', ''),
        'deliverResidence': 'X' if request.form.get('delivery__to') == 'residence address' else '',
        'deliverMailing': 'X' if request.form.get('delivery__to') == 'mailing address' else '',
        'deliverEmail': 'X' if request.form.get('delivery__to') == 'email' else '',
        'genSpecCheck': 'X' if request.form['election__type'] == 'General or Special Election' else '',
        'demPrimCheck': 'X' if request.form['election__type'] == 'Democratic Primary' else '',
        'repPrimCheck': 'X' if request.form['election__type'] == 'Republican Primary' else '',
        'countyCheck': 'X' if 'County' in localities_info.localities[
            request.form['election__locality_gnis']
        ]['locality'] else '',
        'cityCheck': 'X' if 'City' in localities_info.localities[
            request.form['election__locality_gnis']
        ]['locality'] else '',
        'dateMovedMonth': request.form.get('change__date_moved')[5:7],
        'dateMovedDay': request.form.get('change__date_moved')[8:10],
        'dateMovedYear': request.form.get('change__date_moved')[2:4],
        'dateOfElectionMonth': request.form.get('election__date')[5:7],
        'dateOfElectionDay': request.form.get('election__date')[8:10],
        'dateOfElectionYear': request.form.get('election__date')[2:4],
        'todaysDateMonth': todayDate[0:2],
        'todaysDateDay': todayDate[2:4],
        'todaysDateYear': todayDate[4:6],
        'application_ip': request.remote_addr
    }

    registrar_address: str = localities_info.localities[request.form[
        'election__locality_gnis']]['email']
    return data_dict, registrar_address
