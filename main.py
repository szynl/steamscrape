import sys
import requests

def get_link(GAME_NAME):
    '''
    Function has argument game_name and no parameters. Searches for game_name and returns the link if it exists.
    '''
    api_key = "B91FE059AAF809601DA2DA1539B26413"
    url = f"http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        app_list = response.json()["applist"]["apps"]

        for app in app_list:
            if app["name"] == GAME_NAME:
                app_id = app["appid"]
                store_link = f'https://store.steampowered.com/app/{app_id}'
                return store_link
    return None

GAME_NAME = sys.argv[1]
store_link = get_link(GAME_NAME)

while store_link is None:
    print("Game not found. Please enter another game:")
    GAME_NAME = input("")
    store_link = get_link(GAME_NAME)
if store_link is not None:
    print(store_link)
