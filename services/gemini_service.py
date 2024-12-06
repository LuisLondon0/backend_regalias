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

    def generate_human_talent(self, data):
        
        prompt = f"Eres un experto en la planeacion de proyectos. Datos: {data}. En esos datos está la informacion del personal que necesitas y el mes del proyecto que se planea necesitar dicho personal. En ese mismo formato dime el minimo personal que necesito contratar (Si tienen diferentes numeros de meses y son de la misma profresion, los puedes combinar en uno. No tengas en cuenta la experiencia necesaria, pero sí debe aparecer la experiencia cuando los combines). NO JUSTIFIQUES NI AÑADAS NOTAS, SOLO DIME LO QUE PEDI"
        
        response = self.model.generate_content(prompt)

        return(response.text.encode('utf-8').decode('utf-8'))