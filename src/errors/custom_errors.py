from errors import EDYException

class InvalidLoginCredentials(EDYException):
    code = "AD000001"
    
    def __init__(self):
        title = "Invalid Login Credentials"
        http_status = 404
        description = "Not found Pending Transaction"
        translation = "Não há transações pendentes"
        super().__init__(title, self.code, http_status, description, translation)

class ErrorGetProjects(EDYException):
    code = "ED000002"
    
    def __init__(self):
        title = "Error in Get Projects"
        http_status = 500
        description = "There was an error retrieving projects."
        translation = "Houve um erro ao pegar os projetos."
        super().__init__(title, self.code, http_status, description, translation)

class NotFoundToken(EDYException):
    code = "ED000003"
    
    def __init__(self):
        title = "Not Found Token"
        http_status = 404
        description = "Not found token."
        translation = "Token nao encontrado."
        super().__init__(title, self.code, http_status, description, translation)

class ErrorUpdatingProject(EDYException):
    code = "ED000004"
    
    def __init__(self, data):
        title = "Error Updating Project"
        http_status = 500
        description = f"Error updating project: {data}."
        translation = f"Erro ao atualizar projeto: {data}."
        super().__init__(title, self.code, http_status, description, translation)


class HttpError(EDYException):
    code = "ED000005"
    
    def __init__(self, status_code:int, text:str):
        title = "Http Error"
        http_status = 500
        description = f"HTTP Error: Status {status_code} - {text}."
        translation = f"HTTP Error: Status {status_code} - {text}."
        super().__init__(title, self.code, http_status, description, translation)

class InvalidJsonResponse(EDYException):
    code = "ED000006"
    
    def __init__(self, system:str):
        title = "Invalid JSON Eesponse"
        http_status = 500
        description = f"Invalid JSON response from {system}."
        translation = f"Resposta JSON inválida de: {system}."
        super().__init__(title, self.code, http_status, description, translation)


