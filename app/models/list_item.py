import re
from bs4 import BeautifulSoup
from tables.measurements import Measurements


class ListItem:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup
        self.href = self._get_href(self.soup)
        self.price = self._get_price(self.soup)
        self.rooms = self._get_room_num(self.soup)
        self.area = self._get_area(self.soup)

    def _get_href(self, list_item) -> str:
        list_img = list_item.find("td", {"class", "list-img"})
        list_photo = list_img.find("div", {"class", "list-photo"})
        href = list_photo.find("a", href=True)["href"]
        return href

    def _get_price(self, list_item) -> int:
        list_address = list_item.find("td", {"class": "list-adress"})
        list_item_price = list_address.find("span", {"class", "list-item-price"}).text
        return int(re.sub(" |€", "", list_item_price))

    def _get_room_num(self, list_item) -> int:
        list_room_num = list_item.find("td", {"class": "list-RoomNum"}).text.strip()
        return int(list_room_num)

    def _get_area(self, list_item) -> float:
        list_area = list_item.find("td", {"class": "list-AreaOverall"}).text.strip()
        return float(list_area)

    def convert_to_table_model(self) -> Measurements:
        table = Measurements(
            href=self.href,
            price=self.price,
            rooms=self.rooms,
            area=self.area,
        )
        return table
