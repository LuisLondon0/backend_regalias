from database.database import DatabaseConnection
from schemas.fee_value_schema import FeeValueCreate, FeeValueResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeeValueRepository:
    def create_fee_value(self, fee_value: FeeValueCreate) -> FeeValueResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO feevalues (managmentlevel, category, academicsuitability, minimumexperience, monthlyfee, monthlyfeewithtaxes) 
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING feevalueid
                        """, 
                        (fee_value.managmentlevel, fee_value.category, fee_value.academicsuitability, fee_value.minimumexperience, fee_value.monthlyfee, fee_value.monthlyfeewithtaxes)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return FeeValueResponse(
                        id=id, 
                        managmentlevel=fee_value.managmentlevel,
                        category=fee_value.category,
                        academicsuitability=fee_value.academicsuitability,
                        minimumexperience=fee_value.minimumexperience,
                        monthlyfee=fee_value.monthlyfee,
                        monthlyfeewithtaxes=fee_value.monthlyfeewithtaxes
                    )
        except Exception as e:
            logging.error(f"Error creating fee value: {e}")
            raise

    def get_fee_values(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM feevalues")
                    fee_values = cursor.fetchall()
                    if fee_values:
                        return [
                            FeeValueResponse(
                                id=fee_value[0], 
                                managmentlevel=fee_value[1],
                                category=fee_value[2],
                                academicsuitability=fee_value[3],
                                minimumexperience=fee_value[4],
                                monthlyfee=fee_value[5],
                                monthlyfeewithtaxes=fee_value[6]
                            ) 
                            for fee_value in fee_values
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching fee values: {e}")
            raise

    def get_fee_value_by_id(self, fee_value_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM feevalues WHERE feevalueid = %s", (fee_value_id,))
                    fee_value = cursor.fetchone()
                    if fee_value:
                        return FeeValueResponse(
                            id=fee_value[0], 
                            managmentlevel=fee_value[1],
                            category=fee_value[2],
                            academicsuitability=fee_value[3],
                            minimumexperience=fee_value[4],
                            monthlyfee=fee_value[5],
                            monthlyfeewithtaxes=fee_value[6]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching fee value by id {fee_value_id}: {e}")
            raise

    def update_fee_value(self, fee_value_id: int, fee_value: FeeValueCreate) -> FeeValueResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE feevalues 
                        SET managmentlevel = %s, category = %s, academicsuitability = %s, minimumexperience = %s, monthlyfee = %s, monthlyfeewithtaxes = %s 
                        WHERE feevalueid = %s
                        """, 
                        (fee_value.managmentlevel, fee_value.category, fee_value.academicsuitability, fee_value.minimumexperience, fee_value.monthlyfee, fee_value.monthlyfeewithtaxes, fee_value_id)
                    )
                    conn.commit()
                    return FeeValueResponse(
                        id=fee_value_id, 
                        managmentlevel=fee_value.managmentlevel,
                        category=fee_value.category,
                        academicsuitability=fee_value.academicsuitability,
                        minimumexperience=fee_value.minimumexperience,
                        monthlyfee=fee_value.monthlyfee,
                        monthlyfeewithtaxes=fee_value.monthlyfeewithtaxes
                    )
        except Exception as e:
            logging.error(f"Error updating fee value: {e}")
            raise

    def delete_fee_value(self, fee_value_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM feevalues WHERE feevalueid = %s", (fee_value_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No fee value found with id {fee_value_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting fee value: {e}")
            raise