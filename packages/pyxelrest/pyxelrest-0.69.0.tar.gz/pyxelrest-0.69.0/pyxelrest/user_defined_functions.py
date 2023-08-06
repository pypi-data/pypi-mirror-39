"""
This file was generated. DO NOT EDIT manually.
Source file: user_defined_functions.jinja2
Generation date (UTC): 2018-12-03T15:37:11.854296
"""
import xlwings as xw
import datetime
import logging
from pyxelrest.open_api import RequestContent, get_result, convert_to_return_type, get_caller_address, handle_exception

logger = logging.getLogger(__name__)
udf_methods = None  # Will be set after load


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_api_key_header_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_api_key_header_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_api_key_header_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_api_key_or_basic_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_api_key_or_basic_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_api_key_or_basic_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_api_key_query_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_api_key_query_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_api_key_query_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_basic_and_api_key_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_basic_and_api_key_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_basic_and_api_key_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_basic_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_basic_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_basic_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_basic_or_api_key_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_basic_or_api_key_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_basic_or_api_key_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_oauth2_authentication_failure(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_oauth2_authentication_failure]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_oauth2_authentication_failure']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_oauth2_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_oauth2_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_oauth2_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_oauth2_authentication_success_quick_expiry(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_oauth2_authentication_success_quick_expiry]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_oauth2_authentication_success_quick_expiry']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_oauth2_authentication_success_with_custom_response_type(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_oauth2_authentication_success_with_custom_response_type]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_oauth2_authentication_success_with_custom_response_type']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_oauth2_authentication_success_without_response_type(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_oauth2_authentication_success_without_response_type]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_oauth2_authentication_success_without_response_type']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def authenticated_get_oauth2_authentication_timeout(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=authenticated_get_oauth2_authentication_timeout]...".format(excel_caller_address))
    udf_method = udf_methods['authenticated_get_oauth2_authentication_timeout']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_api_key_header_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_api_key_header_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_api_key_header_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_api_key_or_basic_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_api_key_or_basic_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_api_key_or_basic_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_api_key_query_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_api_key_query_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_api_key_query_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_basic_and_api_key_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_basic_and_api_key_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_basic_and_api_key_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_basic_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_basic_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_basic_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_basic_or_api_key_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_basic_or_api_key_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_basic_or_api_key_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_oauth2_authentication_failure(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_oauth2_authentication_failure]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_oauth2_authentication_failure']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_oauth2_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_oauth2_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_oauth2_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_oauth2_authentication_success_quick_expiry(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_oauth2_authentication_success_quick_expiry]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_oauth2_authentication_success_quick_expiry']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_oauth2_authentication_success_with_custom_response_type(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_oauth2_authentication_success_with_custom_response_type]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_oauth2_authentication_success_with_custom_response_type']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_oauth2_authentication_success_without_response_type(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_oauth2_authentication_success_without_response_type]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_oauth2_authentication_success_without_response_type']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_custom_token_name', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_custom_token_name_get_oauth2_authentication_timeout(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_custom_token_name_get_oauth2_authentication_timeout]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_custom_token_name_get_oauth2_authentication_timeout']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_api_key_header_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_api_key_header_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_api_key_header_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_api_key_or_basic_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_api_key_or_basic_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_api_key_or_basic_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_api_key_query_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_api_key_query_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_api_key_query_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_basic_and_api_key_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_basic_and_api_key_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_basic_and_api_key_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_basic_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_basic_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_basic_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_basic_or_api_key_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_basic_or_api_key_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_basic_or_api_key_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_oauth2_authentication_failure(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_oauth2_authentication_failure]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_oauth2_authentication_failure']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_oauth2_authentication_success(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_oauth2_authentication_success]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_oauth2_authentication_success']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_oauth2_authentication_success_quick_expiry(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_oauth2_authentication_success_quick_expiry]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_oauth2_authentication_success_quick_expiry']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_oauth2_authentication_success_with_custom_response_type(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_oauth2_authentication_success_with_custom_response_type]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_oauth2_authentication_success_with_custom_response_type']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_oauth2_authentication_success_without_response_type(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_oauth2_authentication_success_without_response_type]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_oauth2_authentication_success_without_response_type']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='oauth_cutom_response_port', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def oauth_cutom_response_port_get_oauth2_authentication_timeout(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=oauth_cutom_response_port_get_oauth2_authentication_timeout]...".format(excel_caller_address))
    udf_method = udf_methods['oauth_cutom_response_port_get_oauth2_authentication_timeout']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='non_authenticated', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
def non_authenticated_get_without_auth(excel_application=None):
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=non_authenticated_get_without_auth]...".format(excel_caller_address))
    udf_method = udf_methods['non_authenticated_get_without_auth']
    request_content = RequestContent(udf_method, excel_caller_address)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.ret(expand='table')
def pyxelrest_get_url(url, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, excel_application=None):
    """Send a HTTP get request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_get_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_get_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('body',
 doc="""Content of the body.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.arg('parse_body_as',
 doc="""How the body should be sent (['dict', 'dict_list']).""")
@xw.ret(expand='table')
def pyxelrest_post_url(url, body, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, parse_body_as=None, excel_application=None):
    """Send a HTTP post request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_post_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_post_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['body'].validate_required(body, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        udf_method.parameters['parse_body_as'].validate_optional(parse_body_as, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('body',
 doc="""Content of the body.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.arg('parse_body_as',
 doc="""How the body should be sent (['dict', 'dict_list']).""")
@xw.ret(expand='table')
def pyxelrest_put_url(url, body, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, parse_body_as=None, excel_application=None):
    """Send a HTTP put request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_put_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_put_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['body'].validate_required(body, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        udf_method.parameters['parse_body_as'].validate_optional(parse_body_as, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.ret(expand='table')
def pyxelrest_delete_url(url, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, excel_application=None):
    """Send a HTTP delete request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_delete_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_delete_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.ret(expand='table')
def pyxelrest_patch_url(url, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, excel_application=None):
    """Send a HTTP patch request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_patch_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_patch_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.ret(expand='table')
def pyxelrest_head_url(url, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, excel_application=None):
    """Send a HTTP head request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_head_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_head_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)


@xw.func(category='pyxelrest', call_in_wizard=False)
@xw.arg('excel_application', vba='Application')
@xw.arg('url',
 doc="""URL to query.""")
@xw.arg('extra_headers',
 doc="""Extra headers to send in the query.""")
@xw.arg('wait_for_status', numbers=int,
 doc="""HTTP status code to wait for before returning response. 303 means that result is now provided in another URL.""")
@xw.arg('check_interval', numbers=int,
 doc="""Number of seconds to wait before sending a new request. Wait for 30 seconds by default.""")
@xw.arg('auth',
 doc="""Authentication methods to use. (['oauth2_implicit', 'api_key_header', 'api_key_query', 'basic'])""")
@xw.arg('oauth2_auth_url',
 doc="""OAuth2 authorization URL.""")
@xw.arg('oauth2_token_url',
 doc="""OAuth2 token URL.""")
@xw.arg('api_key_name',
 doc="""Name of the field containing API key.""")
@xw.ret(expand='table')
def pyxelrest_options_url(url, extra_headers=None, wait_for_status=None, check_interval=None, auth=None, oauth2_auth_url=None, oauth2_token_url=None, api_key_name=None, excel_application=None):
    """Send a HTTP options request to specified URL."""
    excel_caller_address = get_caller_address(excel_application)
    logger.info("{0} [status=Calling] [function=pyxelrest_options_url]...".format(excel_caller_address))
    udf_method = udf_methods['pyxelrest_options_url']
    request_content = RequestContent(udf_method, excel_caller_address)

    try:
        udf_method.parameters['url'].validate_required(url, request_content)
        udf_method.parameters['extra_headers'].validate_optional(extra_headers, request_content)
        udf_method.parameters['wait_for_status'].validate_optional(wait_for_status, request_content)
        udf_method.parameters['check_interval'].validate_optional(check_interval, request_content)
        udf_method.parameters['auth'].validate_optional(auth, request_content)
        udf_method.parameters['oauth2_auth_url'].validate_optional(oauth2_auth_url, request_content)
        udf_method.parameters['oauth2_token_url'].validate_optional(oauth2_token_url, request_content)
        udf_method.parameters['api_key_name'].validate_optional(api_key_name, request_content)
        request_content.validate()
    except Exception as e:
        logger.exception('{0} Unable to validate parameters.'.format(excel_caller_address))
        return handle_exception(udf_method, str(e), e)
    return get_result(udf_method, request_content, excel_application)
