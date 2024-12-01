from repositories.fee_value_repository import FeeValueRepository
from schemas.fee_value_schema import FeeValueCreate, FeeValueResponse
import logging

class FeeValueService:
    def __init__(self):
        self.repo = FeeValueRepository()

    def create_fee_value(self, fee_value: FeeValueCreate) -> FeeValueResponse:
        if not fee_value.managmentlevel:
            raise ValueError("Management level cannot be empty")
        if not fee_value.category:
            raise ValueError("Category cannot be empty")
        if not fee_value.academicsuitability:
            raise ValueError("Academic suitability cannot be empty")
        if fee_value.minimumexperience < 0:
            raise ValueError("Minimum experience cannot be negative")
        if fee_value.monthlyfee < 0:
            raise ValueError("Monthly fee cannot be negative")
        if fee_value.monthlyfeewithouttaxes < 0:
            raise ValueError("Monthly fee without taxes cannot be negative")

        fee_value.managmentlevel = fee_value.managmentlevel.strip()
        fee_value.category = fee_value.category.strip()
        fee_value.academicsuitability = fee_value.academicsuitability.strip()

        response = self.repo.create_fee_value(fee_value)

        logging.info(f"Fee value created with ID: {response.id}")

        return response

    def get_fee_values(self):
        return self.repo.get_fee_values()

    def get_fee_value_by_id(self, fee_value_id: int):
        if fee_value_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_fee_value_by_id(fee_value_id)

    def update_fee_value(self, fee_value_id: int, fee_value: FeeValueCreate) -> FeeValueResponse:
        if not fee_value.managmentlevel:
            raise ValueError("Management level cannot be empty")
        if not fee_value.category:
            raise ValueError("Category cannot be empty")
        if not fee_value.academicsuitability:
            raise ValueError("Academic suitability cannot be empty")
        if fee_value.minimumexperience < 0:
            raise ValueError("Minimum experience cannot be negative")
        if fee_value.monthlyfee < 0:
            raise ValueError("Monthly fee cannot be negative")
        if fee_value.monthlyfeewithouttaxes < 0:
            raise ValueError("Monthly fee without taxes cannot be negative")

        fee_value.managmentlevel = fee_value.managmentlevel.strip()
        fee_value.category = fee_value.category.strip()
        fee_value.academicsuitability = fee_value.academicsuitability.strip()

        response = self.repo.update_fee_value(fee_value_id, fee_value)

        logging.info(f"Fee value with ID: {fee_value_id} updated")

        return response

    def delete_fee_value(self, fee_value_id: int) -> bool:
        if fee_value_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_fee_value(fee_value_id)

        if success:
            logging.info(f"Fee value with ID: {fee_value_id} deleted")
        else:
            logging.warning(f"Fee value with ID: {fee_value_id} not found")

        return success