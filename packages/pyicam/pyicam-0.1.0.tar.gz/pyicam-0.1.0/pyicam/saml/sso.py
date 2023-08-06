"""
Module defining login utility functions

Copyright (C) 2017-2018 ERT Inc.
"""
__author__ = "Brandon J. Van Vaerenbergh <brandon.vanvaerenbergh@noaa.gov>"

import logging
from itertools import zip_longest

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from . import metadata

logger = logging.getLogger(__name__)

class LoginInvalid(Exception):
    # Single-Sign-On login attempt is invalid
    pass

class LoginSAMLResponseProcessingError(ValueError):
    # problem with response from remote Single-Sign-On authority
    pass

def login(host, port, url_path, settings_path, cert_path, key_path, get_data=dict(), post_data=dict(), https=None):
    """
    Return a dict representing attributes of a logged-in user

    Attributes for the logged in user are extracted from the valid
    SAML2 HTTP response data, sent by the remote Single-Sign-On server.

    Keyword Parameters:
    host  -- String, representing Hostname of server using remote SSO
    port  -- String, representing Port the remote SSO connects to
    url_path  -- String, representing the path component of the URL
      you provided to the remote SSO. E.g.: '/my_service/saml/' if SSO
      is configured to send login successes to
      'https://my.fake_domain/my_service/saml/?acs'
    settings_path  -- String, representing the path to your OneLogin
      settings.json file
    cert_path  -- String,representing path to the OpenSSL PEM formatted
      certificate file identifying the server which uses remote SSO
    key_path  -- String, representing path to the OpenSSL private key
      file used to sign cert_path certifiate file
    get_data  -- dict,representing SAML2 HTTP GET url parameters [E.g.:
      'SAMLResponse']. If post_data parameter is unspecified,a get_data
      parameter value *must* be provided. (Default: empty dict)
    post_data  -- dict, representing SAML2 HTTP POST parameters [E.g.:
      'SAMLResponse']. If get_data parameter is unspecified, a
      post_data parameter value must be provided. (Default: empty dict)
    https  -- (Optional) Boolean, set this if server receives SSO
      responses via https or http

    Exceptions:
    LoginInvalid  -- raised if login failed
    LoginSAMLResponseProcessingError  -- raised if remote response was
      unusable
    """
    req =  { # prepare OneLogin SAML authentication request
        'http_host': host,
        'server_port': port,
        'script_name': url_path,
        'get_data': get_data.copy(),
        'post_data': post_data.copy()
    }
    if https:
        req['https'] = 'off' # Optional https state was set
        if https:
            req['https'] = 'on' # Optional state was True
    with open(cert_path) as cert_file, open(key_path) as key_file:
        cert = cert_file.read()
        key = key_file.read()
    # process
    auth = OneLogin_Saml2_Auth(req, metadata.get_settings_json(settings_path, cert, key))
    auth.process_response()
    errors = auth.get_errors()
    if not errors:
        if auth.is_authenticated():
            # successful login!
            user_attributes = auth.get_attributes()
            # perform requested SAML login action (if any)
            if ('RelayState' in req['post_data'] and
              OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']):
                logger.info('Requested redirect: '+req['post_data']['RelayState'])
                # store processed value, for return
                rs_url = auth.redirect_to(req['post_data']['RelayState'])
                user_attributes['relay_state'] = rs_url
            # log & return
            for attr_name in user_attributes.keys():
                logger.info('{} ==> {}'.format(attr_name, '|| '.join(user_attributes[attr_name])))
            return user_attributes
        else:
          raise LoginInvalid('Not authenticated')
    else:
        errors_oldest_first = errors[::-1]
        errors_and_causes = list(zip_longest(errors_oldest_first, [auth.get_last_error_reason()]))
        raise LoginSAMLResponseProcessingError(str(errors_and_causes))
