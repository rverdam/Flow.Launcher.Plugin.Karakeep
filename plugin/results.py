from pyflowlauncher import Result
from pyflowlauncher.api import open_url, open_setting_dialog, copy_to_clipboard
from pyflowlauncher.icons import SETTINGS, LINK, ERROR, COPY
from pyflowlauncher.settings import settings
from html import unescape

from strip_markdown import strip_markdown
from plugin.karakeep import KarakeepAPI


def _html_text(value, default="") -> str:
    """Return a display-safe string for nullable Karakeep API fields."""
    if value is None:
        return default
    return unescape(str(value))

def error_results(error: str, JsonRPCAction=None):
    """
    Returns a Result representing a Karakeep plugin error.

    :param error: str, the error message
    :param JsonRPCAction: a callable that will be called when the user clicks on the result
    :return: a Result object
    """
    return Result(
        Title="Karakeep Plugin Error",
        SubTitle=error,
        IcoPath=ERROR,
        JsonRPCAction=JsonRPCAction
    )

def no_base_url_results():
    """
    Returns a Result representing a Karakeep plugin error due to no Karakeep Base Address having been set.

    :return: a Result object
    """
    return Result(
        Title="No Karakeep Base Address found!",
        SubTitle="Please enter your Karakeep Base Address in plugin settings.",
        IcoPath=SETTINGS,
        JsonRPCAction=open_setting_dialog()
    )

def no_api_token_results():
    """
    Returns a Result representing a Karakeep plugin error due to no Karakeep API key having been set.

    :return: a Result object
    """
    return Result(
        Title="No API key found!",
        SubTitle="Please enter your Karakeep API key in plugin settings.",
        IcoPath=SETTINGS,
        JsonRPCAction=open_setting_dialog()
    )


def query_result(item) -> Result:
    """Return a Result from a Karakeep API query item.

    This function takes a Karakeep API query item and returns a Result object.
    The Result object contains the title, subtitle, icon path, context data and
    json rpc action of the item.

    :param item: a Karakeep API query item
    :return: a Result object
    """
    content = item.get("content") or {}
    match content.get("type"):
        case "link":
            # If the content type is a link, then we have a title, subtitle and
            # an icon path. The json rpc action is a function that will be
            # called when the user clicks on the result.
            url = (
                content.get("url")
                or f"{settings().get('karakeepBaseAddress')}/dashboard/preview/{item.get('id')}"
            )
            title = content.get("title") or item.get("title") or url or "Untitled link"
            subtitle = _html_text(
                content.get("description"),
                item.get("summary") or item.get("note") or "",
            )
            icon_path = content.get("imageUrl") or content.get("favicon")
            context_data = [{
                "url": url,
                "action": "copy_url"
            },
            {
                 "url": f"{settings().get('karakeepBaseAddress')}/dashboard/preview/{item.get('id')}",
                 "action": "open_url"
            }
            ]
            json_rpc_action = open_url(url)
            return Result(
                Title=title, SubTitle=subtitle, IcoPath=icon_path,
                ContextData=context_data, JsonRPCAction=json_rpc_action
            )
         
        case "text":
            # If the content type is a text, then we have a title, copy text and
            # an icon path. The json rpc action is a function that will be
            # called when the user clicks on the result.
            url = f"{settings().get('karakeepBaseAddress')}/dashboard/preview/{item.get('id')}"
            text = content.get('text') or ""
            firstNoteLine = strip_markdown(text.split('\n')[0])
            title = item.get("title") if item.get("title") else firstNoteLine
            subtitle = firstNoteLine
            title = f"Note: {title or 'Untitled note'}"
            json_rpc_action = open_url(url)
            context_data = [{
                "text": text,
                "action": "copy_markdown_text"
            }]
            return Result(
                Title=title, CopyText=text,
                SubTitle=subtitle,
                IcoPath=COPY,
                ContextData=context_data, JsonRPCAction=json_rpc_action
            )
        
def query_results(Karakeep: KarakeepAPI, query: str):
    """
    Yield a sequence of Result objects for each item found in the Karakeep search query.

    :param Karakeep: a KarakeepAPI instance
    :param query: the search query
    :yield: a sequence of Result objects
    """
    search = Karakeep.search_bookmarks(query) or []
    for item in search:
        content = item.get("content") or {}
        if content.get("type") in ("link", "text"):
            yield query_result(item)

def context_menu_results(data):
    """
    Generate a sequence of Result objects for each item in the context menu data.

    This function processes a list of items, each containing an "action" key,
    and yields a Result object based on the specified action type. The actions
    include copying a URL to the clipboard or copying markdown text.

    :param data: A list of items, each item is a dictionary containing an "action" key
                 and associated data required for the context menu action.
    :yield: A sequence of Result objects corresponding to the actions in the input data.
    """

    for item in data:
        match item.get("action"):
            case "open_url":
                    yield Result(
                        Title="Open item in Karakeep",
                        SubTitle="Open item in Karakeep",
                        IcoPath='./Images/app.png',
                        JsonRPCAction=open_url(item.get("url"))
                    )
            case "copy_url":
                    yield Result(
                        Title="Copy URL to clipboard",
                        SubTitle="Copy URL to clipboard",
                        IcoPath=LINK,
                        JsonRPCAction=copy_to_clipboard(item.get("url"))
                    )
            case "copy_markdown_text":
                    yield Result(
                        Title="Copy Note Text to clipboard",
                        SubTitle="Copy Note Text to clipboard",
                        IcoPath=LINK,
                        JsonRPCAction=copy_to_clipboard(item.get("text"))
                    )                    
