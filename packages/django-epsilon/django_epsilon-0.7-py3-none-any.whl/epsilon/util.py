import time

import requests

from django.conf import settings
from epsilon.schema_profile import schema_profile


class EpsilonException(Exception):
    pass


def epsilon_on():
    if settings.EPSILON_ON is False:
        raise EpsilonException('Epsilon is turned off. Change EPSILON_ON to True')


def epsilon_validate_data(profile):
    if not schema_profile.is_valid(profile):
        raise EpsilonException('Data is invalid.')


def epsilon_authenticate():
    url = settings.EPSILON_API_ENDPOINT + '/OAuth2/AuthenticateVendor/Authorize'
    data = {
        'grant_type': 'vendor',
        'client_id': settings.EPSILON_CLIENT_ID,
        'client_secret': settings.EPSILON_CLIENT_SECRET
    }

    resp = requests.post(url, params=data)
    if resp.status_code != 200:
        raise EpsilonException(f"Epsilon returned code {resp.status_code}. Message: '{resp.text}'")

    try:
        json = resp.json()
        data = {
            'access_token': json['AccessToken'],
            'expires': json['Expires']
        }
        return data
    except Exception as ex:
        raise EpsilonException(ex)


def epsilon_get_transaction_id():
    url = settings.EPSILON_API_ENDPOINT + '/Transaction/GetTransactionID/data'
    resp = requests.post(url)

    if resp.status_code != 200:
        raise EpsilonException(f"Epsilon returned code {resp.status_code}. Message: '{resp.text}'")

    return resp.json()


def epsilon_add_profile(access_token, transaction_id, profile):
    url = settings.EPSILON_API_ENDPOINT + '/Profile/AddProfile/data'

    headers = {
        'Authorization': 'VENDOR %s' % access_token
    }

    data = {
        'ClientID': settings.EPSILON_CLIENT_ID,
        'TransactionID': transaction_id,
        'RecordDate': int(round(time.time() * 1000)),
        'CampaignControlID': settings.EPSILON_CAMPAIGN_CONTROL_ID,
        "GlobalOptOut": "",
        "PreferredChannelCode": "",
        "NamePrefix": "",
        'FirstName': profile['first_name'],
        "MiddleInit": "",
        'LastName': profile['last_name'],
        "Gender": "",
        "NameSuffix": "",
        "BirthDate": profile['date_of_birth'],
        "LanguageCode": "",
        "SalutationID": "",
        "SourceCode": "",
        "AccountVerify": "",
        "AccountVerifyDate": None,
        "CountryCode": "",
        'UserID': "",
        "ProfilePassword": "",
        "ProfilePasswordSalt": "",
        "EncryptionType": 0,
        "Address": {
            "AddressID": "",
            "AddressLine1": "",
            "AddressLine2": "",
            "City": "",
            "State": "",
            "PostalCode": profile['zip_code'],
            "Country": "US",
            "ChannelCode": "AD",
            "ChannelLocationID": "P",
            "DeliveryStatus": "G",
            "Status": "A",
            "IsPreferred": "Y"
        },
        "Emails": [
            {
                "EmailID": "",
                "EmailAddr": profile['email'],
                "ChannelCode": "EM",
                "ChannelLocationID": "H",
                "DeliveryStatus": "G",
                "Status": "A",
                "IsPreferred": "Y"
            }
        ],
        "Phones": [
            {
                "PhoneID": "",
                "PhoneNumber": "",
                "ChannelCode": "PH",
                "ChannelLocationID": "P",
                "DeliveryStatus": "G",
                "Status": "A",
                "IsPreferred": "Y"
            }
        ],
        "SocialProfiles": [
            {
                "SocialProfileID": "",
                "SocialProvider": "",
                "SocialUID": "",
                "SocialAccessToken": "",
                "Status": ""
            }
        ],
        "TrackingInfo": {
            "DomainHash": settings.EPSILON_TRACKING_INFO_DOMAIN_HASH,
            "Timestamp": settings.EPSILON_TRACKING_INFO_TIMESTAMP,
            "UtmSource": settings.EPSILON_TRACKING_UTM_SOURCE,
            "UtmMedium": settings.EPSILON_TRACKING_UTM_MEDIUM,
            "UtmTerm": settings.EPSILON_TRACKING_UTM_TERM,
            "UtmContent": settings.EPSILON_TRACKING_UTM_CONTENT,
            "UtmCampaign": settings.EPSILON_TRACKING_UTM_CAMPAIGN
        },
        "ExternalInfo": "",
        "CultureInfo": ""
    }

    resp = requests.post(url, json=data, headers=headers)
    if resp.status_code != 200:
        raise EpsilonException(f"Epsilon returned code {resp.status_code}. Message: '{resp.text}'")
    try:
        json = resp.json()
        result_type = json['Type']
        profile_id = json['NewProfileID']
        if result_type == 'PROCESSED' and profile_id:
            return profile_id
    except Exception as ex:
        raise EpsilonException(f"Failed to add profile. Response: '{resp.text}'. Exception: {ex}")


def epsilon_add_promotion(access_token, transaction_id, profile_id, profile):
    url = settings.EPSILON_API_ENDPOINT + '/Promotion/AddPromotionResponses/data'

    headers = {
        'Authorization': 'VENDOR %s' % access_token
    }

    data = {
        'ClientID': settings.EPSILON_CLIENT_ID,
        'TransactionID': transaction_id,
        'ProfileID': profile_id,
        'EmailAddress': profile.get('email'),
        'PromotionResponses': [
            {
                'RecordDate': '/Date(%d)/' % int(round(time.time() * 1000)),
                'CampaignControlID': settings.EPSILON_CAMPAIGN_CONTROL_ID,
            }
        ]
    }

    resp = requests.post(url, json=data, headers=headers)
    if resp.status_code != 200:
        raise EpsilonException(f"Epsilon returned code {resp.status_code}. Message: '{resp.text}'")
    try:
        json = resp.json()
        return json['NewPromotionResponseIDs']
    except Exception as ex:
        raise EpsilonException(f"Epsilon failed to add promotion. Message: '{resp.text}'")


def epsilon_add_survey(access_token, transaction_id, profile_id):
    url = settings.EPSILON_API_ENDPOINT + '/Survey/AddSurveyProfileResponses/data'

    headers = {
        'Authorization': 'VENDOR %s' % access_token
    }

    data = {
        'ClientID': settings.EPSILON_CLIENT_ID,
        'TransactionID': transaction_id,
        'ProfileID': profile_id,
        'SurveyProfileResponses': [
            {
                'SurveyQuestionAnswerID': settings.EPSILON_QUESTION_ANSWER_ID,
                'SurveyTextResponse': '',
                'DeleteResponseFlag': 'N',
            }
        ]
    }

    resp = requests.post(url, json=data, headers=headers)
    if resp.status_code != 200:
        raise EpsilonException(f"Epsilon returned code {resp.status_code}. Message: '{resp.text}'")

    json = resp.json()
    result_type = json['Type']
    if result_type != 'PROCESSED':
        raise EpsilonException(f"Epsilon response was not 'PROCESSED'. Message: '{resp.text}'")
