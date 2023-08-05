
class Error(Exception):
    """Error personalizado para mayor control en los programas.

    ATRIBUTOS:

        type = Especifica el tipo de error, en caso de ser un
               error lanzado por el usuario se sugiere utilizar
               el valor 'validacion'.
        message = Descripcion del error.
        control = Variable utilizada por otros programas para
                  validar resultado.
        origen = Funcion donde se dispara el error.
    """

    def __init__(self, _type, _message, _control="", _origin=""):
        self.type = _type
        self.message = _message
        self.control = _control
        self.origen = _origin

    def __str__(self):
        msg = "[%s]....%s - (%s)" % (
            self.type,
            self.message,
            self.control
        )

        return repr(msg)
