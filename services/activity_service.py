from repositories.activity_repository import ActivityRepository
from schemas.activity_schema import ActivityCreate, ActivityResponse
from services.specific_objective_service import SpecificObjectiveService
import logging

class ActivityService:
    def __init__(self):
        self.repo = ActivityRepository()
        self.specific_objective_service = SpecificObjectiveService()

    def create_activity(self, activity: ActivityCreate) -> ActivityResponse:
        specific_objective = self.specific_objective_service.get_specific_objective_by_id(activity.specific_objective_id)
        if not specific_objective:
            raise ValueError("Specific objective does not exist")

        if not activity.description:
            raise ValueError("Description cannot be empty")

        activity.description = activity.description.strip()

        response = self.repo.create_activity(activity)

        logging.info(f"Activity created with ID: {response.id}")

        return response

    def get_activities(self):
        activities = self.repo.get_activities()
        return activities
    
    def get_activity_by_id(self, activity_id: int):
        if activity_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_activity_by_id(activity_id)

    def update_activity(self, activity_id: int, activity: ActivityCreate) -> ActivityResponse:
        specific_objective = self.specific_objective_service.get_specific_objective_by_id(activity.specific_objective_id)
        if not specific_objective:
            raise ValueError("Specific objective does not exist")

        if not activity.description:
            raise ValueError("Description cannot be empty")

        activity.description = activity.description.strip()

        response = self.repo.update_activity(activity_id, activity)

        logging.info(f"Activity with ID: {activity_id} updated")

        return response

    def delete_activity(self, activity_id: int) -> bool:
        if activity_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_activity(activity_id)

        if success:
            logging.info(f"Activity with ID: {activity_id} deleted")
        else:
            logging.warning(f"Activity with ID: {activity_id} not found")

        return success