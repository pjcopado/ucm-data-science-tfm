from shared_kernel.domain.exception import BaseMsgException


class QueryStatusException(BaseMsgException):
    message = "Algo ha ocurrido durante el transcurso de la petición. Vuelva a intentarlo nuevamente más tarde."