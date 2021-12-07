"""
Transforms a non preview url to a Telegram preview url.
"""

def rts(url: str) -> str:
    """
    > rts = Ready to save.

    Recives a url/username and tranforms to a Telegram's preview url.

    examples:

    ```
    [
        'https://t.me/chan',
        'https://telegram.me/chan',
        't.me/chan', 'telegram.me/chan'
        '@chan'
        ]
    ```
    """
    if url.startswith("https://"):
        new_url = "https://t.me/s/" + "/".join(url.split("/")[3:])
    else:
        new_url = "https://t.me/s/" + url[1:]
    return new_url
