from repositories.human_talent_repository import HumanTalentRepository
from schemas.human_talent_schema import HumanTalentCreate, HumanTalentResponse
from services.activity_service import ActivityService
from services.fee_value_service import FeeValueService
import logging

class HumanTalentService:
    def __init__(self):
        self.repo = HumanTalentRepository()
        self.activity_service = ActivityService()
        self.fee_value_service = FeeValueService()

    def create_human_talent(self, human_talent: HumanTalentCreate) -> HumanTalentResponse:
        activity = self.activity_service.get_activity_by_id(human_talent.activityid)
        if not activity:
            raise ValueError("Activity does not exist")

        fee_value = self.fee_value_service.get_fee_value_by_id(human_talent.feevalueid)
        if not fee_value:
            raise ValueError("Fee value does not exist")

        if not human_talent.entity:
            raise ValueError("Entity cannot be empty")
        if not human_talent.position:
            raise ValueError("Position cannot be empty")
        if not human_talent.justification:
            raise ValueError("Justification cannot be empty")
        if human_talent.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        human_talent.entity = human_talent.entity.strip()
        human_talent.position = human_talent.position.strip()
        human_talent.justification = human_talent.justification.strip()

        response = self.repo.create_human_talent(human_talent)

        logging.info(f"Human talent created with ID: {response.id}")

        return response

    def get_human_talents(self):
        return self.repo.get_human_talents()

    def get_human_talent_by_id(self, human_talent_id: int):
        if human_talent_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_human_talent_by_id(human_talent_id)

    def update_human_talent(self, human_talent_id: int, human_talent: HumanTalentCreate) -> HumanTalentResponse:
        activity = self.activity_service.get_activity_by_id(human_talent.activityid)
        if not activity:
            raise ValueError("Activity does not exist")

        fee_value = self.fee_value_service.get_fee_value_by_id(human_talent.feevalueid)
        if not fee_value:
            raise ValueError("Fee value does not exist")

        if not human_talent.entity:
            raise ValueError("Entity cannot be empty")
        if not human_talent.position:
            raise ValueError("Position cannot be empty")
        if not human_talent.justification:
            raise ValueError("Justification cannot be empty")
        if human_talent.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        human_talent.entity = human_talent.entity.strip()
        human_talent.position = human_talent.position.strip()
        human_talent.justification = human_talent.justification.strip()

        response = self.repo.update_human_talent(human_talent_id, human_talent)

        logging.info(f"Human talent with ID: {human_talent_id} updated")

        return response

    def delete_human_talent(self, human_talent_id: int) -> bool:
        if human_talent_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_human_talent(human_talent_id)

        if success:
            logging.info(f"Human talent with ID: {human_talent_id} deleted")
        else:
            logging.warning(f"Human talent with ID: {human_talent_id} not found")

        return success