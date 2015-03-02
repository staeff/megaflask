#!/usr/bin/env python
# coding=utf-8

import json
import requests
from app import app
from flask.ext.babel import gettext
from config import MS_TRANSLATOR_CLIENT_ID, MS_TRANSLATOR_CLIENT_SECRET


def microsoft_translate(text, sourceLang, destLang):
    if MS_TRANSLATOR_CLIENT_ID == "" or MS_TRANSLATOR_CLIENT_SECRET == "":
        return gettext('Error: translation service not configured.')
    try:
        # get access token
        payload = {
            'client_id': MS_TRANSLATOR_CLIENT_ID,
            'client_secret': MS_TRANSLATOR_CLIENT_SECRET,
            'scope': 'http://api.microsofttranslator.com',
            'grant_type': 'client_credentials'}

        r = requests.post('https://datamarket.accesscontrol.windows.net/v2/OAuth2-13', payload)
        token = r.json()[u'access_token']


        # translate
        payload = {
            'appId': 'Bearer ' + token,
            'from': sourceLang,
            'to':   destLang,
            'text': text.encode('utf-8')
        }

        r = requests.get('http://api.microsofttranslator.com/V2/Ajax.svc/Translate', params=payload)
        result = r.content.decode('utf-8-sig')
        response_json = json.loads(u'{{"response":{0}}}'.format(result))
        return response_json["response"]
    except:
        raise
