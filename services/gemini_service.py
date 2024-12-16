import google.generativeai as genai
import os

class gemini_service:
    def __init__(self):
        genai.configure(api_key=os.environ["API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_equipment_software(self, task, result):
        if result is None or result == "":
            prompt = f"Eres un experto en la planeacion de proyectos, dime solamente un hardware (con el siguiente formato: equipo:, características: procesador, ram, almacenamiento), solamente un software (con el siguiente formato: nombre: , caracteristica:) y solamente una justificación (con el siguiente formato: justificación) que se necesite para realizar la siguiente actividad: {task}. NO JUSTIFIQUES NI AÑADAS NOTAS, NO ME CAMBIES LOS FORMATOS NI LE AGREGUES TITULOS O SUBTITULOS A LA RESPUESTA, SOLO DIME LO QUE PEDI"
        else:
            prompt = f"Eres un experto en la planeacion de proyectos, dime solamente un hardware (con el siguiente formato: equipo:, características: procesador, ram, almacenamiento), solamente un software (con el siguiente formato: nombre: , caracteristica:) y solamente una justificación (con el siguiente formato: justificación) que se necesite para realizar la siguiente actividad: {task} y obtener el siguiente resultado: {result}. NO JUSTIFIQUES NI AÑADAS NOTAS, NO ME CAMBIES LOS FORMATOS NI LE AGREGUES TITULOS O SUBTITULOS A LA RESPUESTA, SOLO DIME LO QUE PEDI"
        
        print(prompt)
        response = self.model.generate_content(prompt)
        print(response.text)

        return response.text

    def generate_human_talent(self, data):
        
        prompt = f"Eres un experto en la planeacion de proyectos. Datos: {data}. En esos datos está la informacion del personal que necesitas y el mes del proyecto que se planea necesitar dicho personal. En ese mismo formato dime el minimo personal que necesito contratar (Si tienen diferentes numeros de meses y son de la misma profresion, los puedes combinar en uno, pero debe aparecer especificamente cada mes. No tengas en cuenta la experiencia necesaria, pero sí debe aparecer la experiencia cuando los combines). NO JUSTIFIQUES NI AÑADAS NOTAS, SOLO DIME LO QUE PEDI EN ESE MISMO FORMATO"
        
        response = self.model.generate_content(prompt)

        return(response.text.encode('utf-8').decode('utf-8'))

    def get_human_talent_hours(self, data):
        prompt = f"Eres un experto en la planeacion de proyectos. Datos: {data}. En esos datos está la informacion del personal, las tareas que va a realizar y durante que meses del proyecto se necesita. Estima cuantas horas se necesitará a la semana este personal y cuantas semanas se necesitará por cada año (ten en cuenta los meses que te dí, si te digo mes 15, 16. eso quiere decir que se necesita en el año 2 simplemente, el proyecto es de 3 años). NO JUSTIFIQUES NI AÑADAS NOTAS, SOLO DIME LO QUE PEDI Y SIN DECIMALES. FORMATO: [HORAS A LA SEMANA], [AÑO 1], [AÑO 2], [AÑO 3]"
        
        response = self.model.generate_content(prompt)

        return(response.text.encode('utf-8').decode('utf-8'))
    
    def get_fee_value_talent(self, data, feevalues):
        prompt = f"Eres un experto en la planeacion de proyectos. Datos: {data}. En esos datos está la informacion del personal, las tareas que va a realizar y durante que meses del proyecto se necesita. Segun esta información: {feevalues}, dime el id del cargo donde más encaje el personal. NO JUSTIFIQUES NI AÑADAS NOTAS, SOLO DIME LO QUE PEDI. FORMATO: [id], [monthlyfee]"
        
        response = self.model.generate_content(prompt)

        return(response.text.encode('utf-8').decode('utf-8'))
