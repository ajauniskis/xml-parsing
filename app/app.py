import zlib

from bs4 import BeautifulSoup

from models.list_item import ListItem
from utils.config import DATABASE_URL
from utils.database import create_connection
from utils.logger import logger


def main():
    with create_connection(DATABASE_URL) as conn:
        cur = conn.cursor()

        pages = []

        sql = "SELECT content FROM pages"
        logger.info(f"Executing sql query: {sql}")
        cur.execute(sql)
        for row in cur.fetchall():
            pages.append(zlib.decompress(row[0]))

        cur.close()
        logger.info(f"Query returned {len(pages)} records")

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


if __name__ == "__main__":
    main()
