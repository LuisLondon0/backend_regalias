from repositories.annual_honorariums_repository import AnnualHonorariumsRepository
from schemas.annual_honorariums_schema import AnnualHonorariumsSchema, AnnualHonorariumsResponse
from services.human_talent_service import HumanTalentService
import logging

class AnnualHonorariumsService:
    def __init__(self):
        self.repo = AnnualHonorariumsRepository()
        self.human_talent_service = HumanTalentService()

    def create_annual_honorarium(self, honorarium: AnnualHonorariumsSchema) -> AnnualHonorariumsResponse:
        talent = self.human_talent_service.get_human_talent_by_id(honorarium.talentid)
        if not talent:
            raise ValueError("Talent does not exist")

        if honorarium.honorariumamount < 0:
            raise ValueError("Honorarium amount cannot be negative")
        if honorarium.totalamount < 0:
            raise ValueError("Total amount cannot be negative")
        if honorarium.year <= 0:
            raise ValueError("Year must be a positive integer")
        if honorarium.weekofyears <= 0:
            raise ValueError("Week of years must be a positive integer")

        honorarium.hourvalue = honorarium.hourvalue.strip()

        response = self.repo.create_annual_honorarium(honorarium)

        logging.info(f"Annual honorarium created with ID: {response.id}")

        return response

    def get_annual_honorariums(self):
        return self.repo.get_annual_honorariums()

    def get_annual_honorarium_by_id(self, honorarium_id: int):
        if honorarium_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_annual_honorarium_by_id(honorarium_id)

    def update_annual_honorarium(self, honorarium_id: int, honorarium: AnnualHonorariumsSchema) -> AnnualHonorariumsResponse:
        talent = self.human_talent_service.get_human_talent_by_id(honorarium.talentid)
        if not talent:
            raise ValueError("Talent does not exist")

        if honorarium.honorariumamount < 0:
            raise ValueError("Honorarium amount cannot be negative")
        if honorarium.totalamount < 0:
            raise ValueError("Total amount cannot be negative")
        if honorarium.year <= 0:
            raise ValueError("Year must be a positive integer")
        if honorarium.weekofyears <= 0:
            raise ValueError("Week of years must be a positive integer")

        honorarium.hourvalue = honorarium.hourvalue.strip()

        response = self.repo.update_annual_honorarium(honorarium_id, honorarium)

        logging.info(f"Annual honorarium with ID: {honorarium_id} updated")

        return response

    def delete_annual_honorarium(self, honorarium_id: int) -> bool:
        if honorarium_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_annual_honorarium(honorarium_id)

        if success:
            logging.info(f"Annual honorarium with ID: {honorarium_id} deleted")
        else:
            logging.warning(f"Annual honorarium with ID: {honorarium_id} not found")

        return success