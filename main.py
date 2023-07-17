import requests
from bs4 import BeautifulSoup as bs

def get_link(GAME_NAME):
    '''
    Function has argument GAME_NAME and no parameters.
    Searches for GAME_NAME and returns the link if it exists.
    '''
    key = "B91FE059AAF809601DA2DA1539B26413"
    url = f"http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={key}"
    response = requests.get(url)

    if response.status_code == 200:
        app_list = response.json()["applist"]["apps"]

        for app in app_list:
            if app["name"] == GAME_NAME:
                app_id = app["appid"]
                store_link = f"https://store.steampowered.com/app/{app_id}"
                return store_link


def search_game(GAME_LINK):
    '''
    Function has argument GAME_LINK and no parameters.
    Accesses GAME_LINK and prints the relevant game information.
    '''
    response = requests.get(GAME_LINK)
    soup = bs(response.content, "html.parser")

    game_name = "apphub_AppName"
    name = soup.find(class_=game_name)

    game_review = "game_review_summary positive"
    reviews = soup.find_all(class_=game_review)

    game_date = "date"
    date = soup.find(class_=game_date)

    game_studios = "dev_row"
    studios = soup.find_all(class_=game_studios)
    developer = studios[0].text.strip().split(":\n\n")
    publisher = studios[1].text.strip().split(":\n\n")

    game_price = "game_purchase_price price"
    current_price = str(soup.find(class_=game_price)).strip().replace(" ", "")
    if current_price.find("Free") != -1:
        price = "A$0.00"
    else:
        start = current_price.find("A$")
        end = current_price.find("</div>")
        price = current_price[start:end]

    print(f'''\nGame title: {name.text}
Recent reviews: {reviews[0].text}
All reviews: {reviews[1].text}
Release date: {date.text}
Developer: {developer[1]}
Publisher: {publisher[1]}
Price: {price}\n''')

while __name__ == "__main__":
    GAME_NAME = input("Enter game title to search (case-sensitive): ")
    if GAME_NAME == "exit":
        exit()
    else:
        store_link = get_link(GAME_NAME)

        while store_link is None:
            print("Game not found.\n")
            GAME_NAME = input("Enter game title to search (case-sensitive): ")
            store_link = get_link(GAME_NAME)

        search_game(store_link)
