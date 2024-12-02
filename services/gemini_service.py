import google.generativeai as genai
import os

class gemini_service:
    def __init__(self):
        genai.configure(api_key=os.environ["API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_equipment_software(self, activities):
        for activity in activities:
            if activity["activity"] == "generate_equipment_software":
                prompt = f"Eres un experto en la planeacion de proyectos, dime solamente un hardware (con el siguiente formato: procesador, ram, almacenamiento, graficos) y solamente un software (con el siguiente formato: nombre, una caracteristica) que se necesite para realizar la siguiente actividad: {activity}. NO JUSTIFIQUES NI AÑADAS NOTAS, SOLO DIME LO QUE PEDI"
                
                response = self.model.generate_content(prompt)

                print(response)