
class Error(Exception):
    """Error personalizado para mayor control en los programas.

    ATRIBUTOS:

        type = Especifica el tipo de error, en caso de ser un
               error lanzado por el usuario se sugiere utilizar
               el valor 'validacion'.
        origen = Funcion donde se dispara el error.
        control = Variable utilizada por otros programas para
                  validar resultado.
        message = Descripcion del error.
    """

    def __init__(self, _type, _message, _origin="", _control=""):
        self.type = _type
        self.message = _message
        self.origen = _origin
        self.control = _control

    def __str__(self):
        msg = "[%s]....%s - (%s)" % (
            self.type,
            self.message,
            self.origen
        )

        return repr(msg)
