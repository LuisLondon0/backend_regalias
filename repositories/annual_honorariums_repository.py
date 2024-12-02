from database.database import DatabaseConnection
from schemas.annual_honorariums_schema import AnnualHonorariumsSchema, AnnualHonorariumsResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnnualHonorariumsRepository:
    def create_annual_honorarium(self, honorarium: AnnualHonorariumsSchema) -> AnnualHonorariumsResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO annualhonorariums (talentid, honorariumamount, hourvalue, year, weekofyears, totalamount) 
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING honorariumid
                        """, 
                        (honorarium.talentid, honorarium.honorariumamount, honorarium.hourvalue, honorarium.year, honorarium.weekofyears, honorarium.totalamount)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return AnnualHonorariumsResponse(
                        id=id, 
                        talentid=honorarium.talentid,
                        honorariumamount=honorarium.honorariumamount,
                        hourvalue=honorarium.hourvalue,
                        year=honorarium.year,
                        weekofyears=honorarium.weekofyears,
                        totalamount=honorarium.totalamount
                    )
        except Exception as e:
            logging.error(f"Error creating annual honorarium: {e}")
            raise

    def get_annual_honorariums(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM annualhonorariums")
                    honorariums = cursor.fetchall()
                    if honorariums:
                        return [
                            AnnualHonorariumsResponse(
                                id=honorarium[0], 
                                talentid=honorarium[1],
                                honorariumamount=honorarium[2],
                                hourvalue=honorarium[3],
                                year=honorarium[4],
                                weekofyears=honorarium[5],
                                totalamount=honorarium[6]
                            ) 
                            for honorarium in honorariums
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching annual honorariums: {e}")
            raise

    def get_annual_honorarium_by_id(self, honorarium_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM annualhonorariums WHERE honorariumid = %s", (honorarium_id,))
                    honorarium = cursor.fetchone()
                    if honorarium:
                        return AnnualHonorariumsResponse(
                            id=honorarium[0], 
                            talentid=honorarium[1],
                            honorariumamount=honorarium[2],
                            hourvalue=honorarium[3],
                            year=honorarium[4],
                            weekofyears=honorarium[5],
                            totalamount=honorarium[6]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching annual honorarium by id {honorarium_id}: {e}")
            raise

    def update_annual_honorarium(self, honorarium_id: int, honorarium: AnnualHonorariumsSchema) -> AnnualHonorariumsResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE annualhonorariums 
                        SET talentid = %s, honorariumamount = %s, hourvalue = %s, year = %s, weekofyears = %s, totalamount = %s 
                        WHERE honorariumid = %s
                        """, 
                        (honorarium.talentid, honorarium.honorariumamount, honorarium.hourvalue, honorarium.year, honorarium.weekofyears, honorarium.totalamount, honorarium_id)
                    )
                    conn.commit()
                    return AnnualHonorariumsResponse(
                        id=honorarium_id, 
                        talentid=honorarium.talentid,
                        honorariumamount=honorarium.honorariumamount,
                        hourvalue=honorarium.hourvalue,
                        year=honorarium.year,
                        weekofyears=honorarium.weekofyears,
                        totalamount=honorarium.totalamount
                    )
        except Exception as e:
            logging.error(f"Error updating annual honorarium: {e}")
            raise

    def delete_annual_honorarium(self, honorarium_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM annualhonorariums WHERE honorariumid = %s", (honorarium_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No annual honorarium found with id {honorarium_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting annual honorarium: {e}")
            raise