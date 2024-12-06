from repositories.human_talent_repository import HumanTalentRepository
from schemas.human_talent_schema import HumanTalentCreate, HumanTalentResponse
from services.activity_service import ActivityService
from services.fee_value_service import FeeValueService
import logging, re

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

        if not human_talent.position:
            raise ValueError("Position cannot be empty")
        if not human_talent.justification:
            raise ValueError("Justification cannot be empty")
        if human_talent.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

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
    
    def create_budget(self, id):
        try:
            from services.activity_service import ActivityService
            from services.task_service import TaskService
            from services.gemini_service import gemini_service

            activity_service = ActivityService()
            task_service = TaskService()
            gemini_service = gemini_service()

            activities = activity_service.get_activities_ids_by_project_id(id)

            #for activity in activities[2:4]:
            for activity in activities[:1]:
                tasks = task_service.get_tasks_by_activity(activity)
                data = ""
                for task in tasks:
                    data = data + f"[Personnel: {task["required_personnel"]}, Months: {task["months_required"]}], "
                response = gemini_service.generate_human_talent(data)

                entries = re.findall(r'\[Personnel: (.*?)\]', response)

                processed_entries = []
                for entry in entries:
                    personnel_match = re.match(r'- (.+?) \((\d+)\): (.+?), Months: (.+)', entry)
                    if personnel_match:
                        role = personnel_match.group(1).strip()
                        quantity = int(personnel_match.group(2))
                        description = personnel_match.group(3).strip()
                        months = [int(m.strip()) for m in personnel_match.group(4).split(',') if m.strip().isdigit()]
                    else:
                        parts = re.split(r', Months: ', entry)
                        role_quantity_match = re.match(r'- (.+?) \((\d+)\)', parts[0])
                        if role_quantity_match:
                            role = role_quantity_match.group(1).strip()
                            quantity = int(role_quantity_match.group(2))
                        else:
                            role = parts[0].strip('- ').strip()
                            quantity = 1
                        description = ''
                        months = [int(m.strip()) for m in parts[1].split(',') if m.strip().isdigit()] if len(parts) > 1 else []
                    processed_entries.append({
                        'role': role,
                        'quantity': quantity,
                        'description': description,
                        'months': months
                    })

                for entry in processed_entries:
                    human_talent = HumanTalentCreate(
                        activityid=activity,
                        feevalueid=1,
                        entity="",
                        position=entry['role'],
                        justification=entry['description'] if entry['description'] else "N/A",
                        quantity=entry['quantity']
                    )
                    self.create_human_talent(human_talent)
            return True
        except Exception as e:
            logging.error(f"Error creating budget: {e}")
            raise