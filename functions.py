import json


def buildJSON(request):
    absentee_first_name = request.form['name__first']
    absentee_middle_name = request.form['name__middle']
    absentee_last_name = request.form['name__last']
    absentee_suffix = request.form['name__suffix']
    absentee_ssn = request.form['name__ssn']

    election_type = request.form['election__type']
    election_date = request.form['election__date']
    election_locality = request.form['election__locality_gnis']

    absentee_reason = request.form['reason__code']
    absentee_reason_documentation = request.form['reason__documentation']

    absentee_birth_year = request.form['birth_year']
    absentee_telephone = request.form['more_info__telephone']
    absentee_email = request.form['more_info__email_fax']

    absentee_street_address = request.form['address__street']
    absentee_unit = request.form['address__unit']
    absentee_city = request.form['address__city']
    absentee_state = request.form['address__state']
    absentee_zip = request.form['address__zip']

    ballot_delivery_destination = request.form['delivery__to']
    delivery_street_address = request.form['delivery__street']
    delivery_unit = request.form['delivery__unit']
    delivery_city = request.form['delivery__city']
    delivery_country = request.form['country']
    delivery_state = request.form['deliv-state']
    delivery_zip = request.form['delivery__zip']
    # delivery_state_country = request.form['delivery__state_or_country']

    absentee_former_name = request.form['change__former_name']
    absentee_former_address = request.form['change__former_address']
    absentee_date_moved = request.form['change__date_moved']

    absentee_assistance = request.form['assistance__assistance']

    assistant_signed = request.form['assistant__signed']
    assistant_name = request.form['assistant__name']
    assistant_street_address = request.form['assistant__street']
    assistant_unit = request.form['assistant__unit']
    assistant_city = request.form['assistant__city']
    assistant_state = request.form['assistant__state']
    assistant_zip = request.form['assistant__zip']
    assistant_signature = request.form['assistant__sig']

    absentee_agreement = request.form['checkbox']
    absentee_signature_date = request.form['signature__date']
    absentee_signature = request.form['signature__signed']
