from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOrdersByStore(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                FROM orders o
                WHERE o.store_id = %s"""

        cursor.execute(query, (store.store_id,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCouples(store, idMapOrders):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT o1.id or1, o2.id or2, o1.num_oggetti+o2.num_oggetti as tot_oggetti
                FROM (SELECT o.order_id as id, o.order_date as order_date, SUM(oi.quantity) as num_oggetti
                    FROM orders o
                    JOIN order_items oi ON o.order_id=oi.order_id 
                    WHERE o.store_id = %s
                    GROUP BY o.order_id, o.order_date) as o1, 
                    (SELECT o.order_id as id, o.order_date as order_date, SUM(oi.quantity) as num_oggetti
                    FROM orders o
                    JOIN order_items oi ON o.order_id=oi.order_id 
                    WHERE o.store_id = %s
                    GROUP BY o.order_id, o.order_date) as o2
                WHERE o1.order_date < o2.order_date"""

        cursor.execute(query, (store.store_id, store.store_id))

        for row in cursor:
            results.append((idMapOrders[row["or1"]], idMapOrders[row["or2"]], row["tot_oggetti"]))

        cursor.close()
        conn.close()
        return results