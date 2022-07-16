import json
import zlib
from collections import OrderedDict
from sqlite3 import Cursor
from typing import List, Tuple

from bs4 import BeautifulSoup

from models.list_item import ListItem
from utils.config import DATABASE_URL
from utils.database import create_connection
from utils.logger import logger


def get_avg_price(cursor: Cursor) -> float:
    sql = "SELECT AVG(price) FROM measurements"

    logger.info(f"Executing sql query: {sql}")
    result = cursor.execute(sql).fetchall()

    return result[0][0]


def get_avg_price_3_room(cursor: Cursor) -> Tuple[int, float]:
    sql_count = "SELECT COUNT(*) FROM measurements WHERE rooms = 3"
    logger.info(f"Executing sql query: {sql_count}")
    count_result = cursor.execute(sql_count).fetchall()

    sql_avg = "SELECT AVG(price) FROM measurements WHERE rooms = 3"
    logger.info(f"Executing sql query: {sql_avg}")
    avg_result = cursor.execute(sql_avg).fetchall()

    return count_result[0][0], avg_result[0][0]


def get_top_area(
    cursor: Cursor,
    top_number: int,
) -> List[OrderedDict[str, str | float | int]]:
    sql = f"SELECT obj_id, area, price, rooms, url FROM measurements ORDER BY area DESC LIMIT {top_number}"
    logger.info(f"Executing sql query: {sql}")
    result = cursor.execute(sql).fetchall()

    objects = []

    for record in result:
        r = OrderedDict()
        r["obj_id"] = record[0]
        r["area"] = record[1]
        r["price"] = record[2]
        r["rooms"] = record[3]
        r["url"] = record[4]
        objects.append(r)

    return objects


def main():
    with create_connection(DATABASE_URL) as conn:
        cur = conn.cursor()

        pages = []

        sql = "SELECT content FROM pages"
        logger.info(f"Executing sql query: {sql}")
        cur.execute(sql)
        for row in cur.fetchall():
            pages.append(zlib.decompress(row[0]))

        logger.info(f"Query returned {len(pages)} records")
        cur.close()

    total = 0
    i = 1
    for page in pages:
        logger.info(f"Parsing page {i}/{len(pages)}")

        soup = BeautifulSoup(page, "html.parser")
        list_rows = soup.findAll("tr", {"class", "list-row"})

        logger.info(f"Found {len(list_rows)} items in page {i}/{len(pages)}")

        k = 0
        for list_row in list_rows:
            try:
                list_item = ListItem(list_row)

                table_model = list_item.convert_to_table_model()
                table_model.create_entry()  # pyright: ignore [reportGeneralTypeIssues]
                k += 1
            except AttributeError as e:
                logger.warning(f"Could not parse item: {list_row} to {ListItem}")

        total += k
        logger.info(f"Page {i}/{len(pages)} done. Added {k} items")
        i += 1

    logger.info(f"All pages parsed. Total items added: {total}")

    with create_connection(DATABASE_URL) as conn:
        cur = conn.cursor()

        logger.info(f"Running sql queries for analysis")
        avg_price = get_avg_price(cur)
        avg_price_3_room = get_avg_price_3_room(cur)
        top_area_5 = get_top_area(cur, 5)

        cur.close()

    logger.info(
        f"Average price of real estate objects in the dataset is: {round(avg_price, 2)} €"
    )
    logger.info(
        f"There are {avg_price_3_room[0]} real estate object that have 3 rooms with the average price of {round(avg_price_3_room[1], 2)} €"
    )
    logger.info(
        f"Top five biggest real estate objects:\n{json.dumps(top_area_5, indent=4)}"
    )


if __name__ == "__main__":
    main()
