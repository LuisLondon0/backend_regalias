from repositories.project_repository import ProjectRepository
from schemas.project_schema import ProjectCreate, ProjectResponse
from schemas.specific_objective_schema import SpecificObjectiveCreate, SpecificObjectiveResponse
from schemas.activity_schema import ActivityCreate, ActivityResponse
from schemas.task_schema import TaskCreate, TaskResponse
from schemas.month_schema import MonthCreate, MonthResponse
from schemas.schedule_schema import ScheduleCreate, ScheduleResponse
from fastapi import UploadFile, HTTPException
from typing import List
import pandas as pd
import logging

class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()

    def create_project(self, project: ProjectCreate) -> ProjectResponse:
        if not project.description:
            raise ValueError("Description cannot be empty")

        project.description = project.description.strip()

        response = self.repo.create_project(project)

        logging.info(f"Project created with ID: {response.id}")

        return response
    
    async def create_projects_from_excel(self, file: UploadFile) -> List[ProjectResponse]:
        from services.specific_objective_service import SpecificObjectiveService
        from services.activity_service import ActivityService
        from services.task_service import TaskService
        from services.month_service import MonthService
        from services.schedule_service import ScheduleService

        specific_objective_service = SpecificObjectiveService()
        activity_service = ActivityService()
        task_service = TaskService()
        month_service = MonthService()
        schedule_service = ScheduleService()

        try:
            df = pd.read_excel(file.file, header=1)

            col_index = df.columns.get_loc(1)
            df_schedule = df.iloc[:, col_index:]

            first_empty_index = df["Num_tarea"].isna().idxmax()

            columns_of_interest = ['Problema', 'Objetivo general', 'Objetivos Específicos', 'Actividades', 'Tareas', 'Responsable \n(Entidad)', 'Personal requerido (perfiles y descripción)', 'Resultados de la actividad', 'Productos \n(Consultar manual sector 39 programa 3906)', 'Medio de verificación \n(del cumplimiento de la actividad)', 'Indicador de producto\n(colocar la meta a la que se quiere llegar con el producto por ejemplo # de estudiantes de doctorado)', 'Medio de verificación', 'Requerimientos técnicos, tecnológicos, logísticos']
            filtered_df = df[columns_of_interest].iloc[:first_empty_index]
            df_schedule = df_schedule.iloc[:first_empty_index]

            df_schedule = df_schedule.apply(lambda row: row[row == "x"].index.to_list(), axis=1)

            problem = filtered_df["Problema"].dropna().tolist()
            general_objective = filtered_df["Objetivo general"].dropna().tolist()

            project_create = ProjectCreate(
                description=problem[0],
                generalobjective=general_objective[0],
                projectdocument=None,
                totalsgr=None,
                totalduration=None
            )
            project_response = self.create_project(project_create)

            specific_objectives = filtered_df["Objetivos Específicos"].dropna().tolist()
            specific_objectives_index = filtered_df["Objetivos Específicos"].dropna().index.tolist()

            activities = filtered_df["Actividades"].dropna().tolist()
            activities_index = filtered_df["Actividades"].dropna().index.tolist()

            for index, row in filtered_df.iterrows():
                if index in specific_objectives_index:
                    act_specific_objectives = specific_objectives.pop(0)
                    specific_objective_create = SpecificObjectiveCreate(
                        description=act_specific_objectives,
                        project_id=project_response.id
                    )
                    specific_objective_response = specific_objective_service.create_specific_objective(specific_objective_create)
                
                if index in activities_index:
                    act_activities = activities.pop(0)
                    activity_create = ActivityCreate(
                        specificobjective_id=specific_objective_response.id,
                        description=act_activities,
                        product=row["Productos \n(Consultar manual sector 39 programa 3906)"],
                        verificationmethod=row["Medio de verificación \n(del cumplimiento de la actividad)"],
                        productindicator=row["Indicador de producto\n(colocar la meta a la que se quiere llegar con el producto por ejemplo # de estudiantes de doctorado)"],
                    )
                    activity_response = activity_service.create_activity(activity_create)

                task_create = TaskCreate(
                    activity_id=activity_response.id,
                    description=row["Tareas"],
                    responsible=row["Responsable \n(Entidad)"],
                    requiredstaff=row["Personal requerido (perfiles y descripción)"],
                    activityresult=row["Resultados de la actividad"],
                    technical_requirement=row["Requerimientos técnicos, tecnológicos, logísticos"]
                )
                task_response = task_service.create_task(task_create)
            
                schedule = df_schedule.get(index)

                for i in schedule:
                    month_create = MonthCreate(
                        task_id=task_response.id,
                        month=i
                    )
                    month_response = month_service.create_month(month_create)

                    schedule_create = ScheduleCreate(
                        month_id=month_response.id,
                        task_id=task_response.id
                    )
                    schedule_service.create_schedule(schedule_create)

            logging.info(f"Project created from Excel file")
            return True
        except Exception as e:
            logging.error(f"Error processing Excel file: {e}")
            raise HTTPException(status_code=400, detail="Error processing Excel file")

    def get_projects(self):
        projects = self.repo.get_projects()
        return projects

    def get_project_by_id(self, project_id: int) -> ProjectResponse:
        if project_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_project_by_id(project_id)

    def update_project(self, project_id: int, project: ProjectCreate) -> ProjectResponse:
        if not project.description:
            raise ValueError("Description cannot be empty")

        project.description = project.description.strip()

        response = self.repo.update_project(project_id, project)

        logging.info(f"Project with ID: {project_id} updated")

        return response

    def delete_project(self, project_id: int) -> bool:
        if project_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_project(project_id)

        if success:
            logging.info(f"Project with ID: {project_id} deleted")
        else:
            logging.warning(f"Project with ID: {project_id} not found")

        return success