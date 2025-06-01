from pyflowlauncher import Plugin, send_results
from pyflowlauncher.api import open_setting_dialog
from pyflowlauncher.settings import settings
from pyflowlauncher.icons import RECYCLEBIN, SETTINGS, LINK
from requests import HTTPError

from .karakeep import KarakeepAPI
from results import query_results, context_menu_results, no_api_token_results, no_base_url_results, error_results

plugin = Plugin()

@plugin.on_method
def query(query: str):
    baseUrl = settings().get('karakeepBaseAddress')
    apiKey = settings().get('karakeepApiKey')
    
    if not baseUrl:
        return send_results([no_base_url_results()])
    
    if not apiKey:
        return send_results([no_api_token_results()])
    
    karakeep_api = KarakeepAPI(base_url=baseUrl, api_key=apiKey)
    
    return send_results(
        query_results (karakeep_api, query)     
    )

@plugin.on_method
def context_menu(data):
    return send_results(context_menu_results(data))

@plugin.on_except(HTTPError)
def http_error(error: HTTPError):
    match error.response.status_code:
        case 401:
            return send_results([error_results("Unauthorized: Invalid API key. Click to open settings.", JsonRPCAction=open_setting_dialog())])
        case 404:
            return send_results([error_results("API Endpoint Not found (Invalid URL?). Click to open settings.", JsonRPCAction=open_setting_dialog())])
        case _:
            return send_results([error_results(str(error))])

@plugin.on_except(ConnectionError)
def connection_error(error: ConnectionError):
    match error:
        case _:
            return send_results([error_results("Connection error. Click to open settings.", JsonRPCAction=open_setting_dialog())])