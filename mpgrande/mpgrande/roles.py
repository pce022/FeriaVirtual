from rolepermissions.roles import AbstractUserRole

#EJEMPLOS DE PRUEBA
class Entrada(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }

#GRUPOS DE PERMISOS
class Externo(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }       

class Interno(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }      

class Productor(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }       
class Transportista(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }      
class Administrador(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }       

class Consultor(AbstractUserRole):
    available_permissions = {
        'create_record': True,
    }           