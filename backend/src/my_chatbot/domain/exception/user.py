from shared_kernel.domain.exception import BaseMsgException


class UserNotFoundException(BaseMsgException):
    message = "Usuario y/o contraseña erroneos."

class UserExist(BaseMsgException):
    message = "El usuario ya existe."
