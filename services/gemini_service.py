import google.generativeai as genai
import os

class gemini_service:
    def __init__(self):
        genai.configure(api_key=os.environ["API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_equipment_software(self, task, result):

        prompt = f"Eres un experto en la planeacion de proyectos, dime solamente un hardware (con el siguiente formato: equipo:, características: procesador, ram, almacenamiento), solamente un software (con el siguiente formato: nombre: , caracteristica:) y solamente una justificación (con el siguiente formato: justificación) que se necesite para realizar la siguiente actividad: {task} y obtener el siguiente resultado: {result}. NO JUSTIFIQUES NI AÑADAS NOTAS, NO ME CAMBIES LOS FORMATOS NI LE AGREGUES TITULOS O SUBTITULOS A LA RESPUESTA, SOLO DIME LO QUE PEDI"
        
        response = self.model.generate_content(prompt)
        print(response.text)

        return response.text

        

        