from database.DB_connect import DBConnect
from model.edges import Edge
from model.retailers import Retailer


class DAO():
    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()
        curs = conn.cursor(dictionary = True)

        query = """select distinct country
                from go_retailers gr"""

        curs.execute(query)
        result = []
        for row in curs:
            result.append(row["country"])
        curs.close()
        conn.close()
        return result

    @staticmethod
    def getRetailers(nazione):
        conn = DBConnect.get_connection()
        curs = conn.cursor(dictionary=True)

        query = """select *
                    from go_retailers gr 
                    where Country = %s"""

        curs.execute(query, (nazione,))
        result = []
        for row in curs:
            result.append(Retailer(**row))
        curs.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(nazione, anno):
        conn = DBConnect.get_connection()
        curs = conn.cursor(dictionary=True)

        query = """select t1.retailer_code as r1, t2.retailer_code as r2, count(*) as weight
                    from
                        (select distinct gds.Retailer_code, gds.Product_number
                        from go_daily_sales gds, go_retailers gr 
                        where YEAR(gds.`Date`) = %s
                        and gds.Retailer_code = gr.Retailer_code
                        and gr.Country = %s) t1,
                        (select distinct gds2.Retailer_code, gds2.Product_number
                        from go_daily_sales gds2, go_retailers gr2
                        where YEAR(gds2.`Date`) = %s
                        and gds2.Retailer_code = gr2.Retailer_code
                        and gr2.Country = %s) t2
                    where t1.product_number = t2.product_number
                    and t1.retailer_code < t2.retailer_code
                    group by t1.retailer_code, t2.retailer_code"""

        curs.execute(query, (anno, nazione, anno, nazione))
        result = []
        for row in curs:
            result.append(Edge(**row))
        curs.close()
        conn.close()
        return result