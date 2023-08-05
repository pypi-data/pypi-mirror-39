# Python's Libraries
# import re
# import shutil
import os

# Own's Libraries
from stxtools.data import Error


class Folder(object):

    def __init__(self, _abspath):
        self.abspath = _abspath

    def __str__(self):
        return self.abspath

    def is_Exist(self, _origin="", _raise_error_on=None):
        value = os.path.exists(self.abspath)
        if value:
            if _raise_error_on:
                raise Error(
                    "validacion",
                    "La carpeta '%s' ya existe" % (self.abspath),
                    "carpeta existe",
                    _origin
                )
            return True
        else:
            if _raise_error_on is False:
                raise Error(
                    "validacion",
                    "La carpeta '%s' no existe" % (self.abspath),
                    "carpeta no existe",
                    _origin,
                )
            return False

    def get_Basepath(self):
        basepath = os.path.abspath(
            os.path.join(
                self.abspath,
                os.pardir
            )
        )
        return basepath

    def create(self, _raise_errors=False, _create_struct=False):
        folder_base = Folder(self.get_Basepath())

        if _raise_errors:
            if _create_struct is False:
                folder_base.is_Exist(_raise_error_on=False)

            self.is_Exist(_raise_error_on=True)
            os.makedirs(self.abspath)
            print ("Carpeta '%s' creada con exito" % (self.abspath))
            return True
        else:
            try:
                if _create_struct is False:
                    if folder_base.is_Exist() is False:
                        error = Error(
                            "validacion",
                            "No existe el directorio padre '%s'" % (
                                folder_base
                            ),
                            "no existe directorio",
                            ""
                        )
                        print(error)
                        return False

                os.makedirs(self.abspath)
                print ("Carpeta '%s' creada con exito" % (self.abspath))

            except Exception as error:
                print(str(error))

    def get_QtyFiles(self, num_levels=None):
        self.is_Exist(_raise_error_on=False)

        elements = os.walk(self.abspath)
        qty = 0
        level = 0
        for directory_path, list_dirnames, list_filenames in elements:
            qty += len(list_filenames)

            level += 1
            if num_levels == level:
                break

        return qty

    def get_QtyFolders(self, num_levels=None):
        self.is_Exist(_raise_error_on=False)

        elements = os.walk(self.abspath)
        qty = 0
        level = 0
        for directory_path, list_dirnames, list_filenames in elements:
            qty += len(list_dirnames)

            level += 1
            if num_levels == level:
                break

        return qty

    def get_QtyElements(self, num_levels=None):
        self.is_Exist(_raise_error_on=False)

        elements = os.walk(self.abspath)
        qty_files = 0
        qty_folders = 0
        level = 0
        for directory_path, list_dirnames, list_filenames in elements:
            qty_files += len(list_dirnames)
            qty_folders += len(list_filenames)

            level += 1
            if num_levels == level:
                break

        return qty_folders, qty_files

    def get_Files(self, num_levels=None):
        self.is_Exist(_raise_error_on=False)

        level = 0
        list_files = []
        elements = os.walk(self.abspath)
        for directory_path, list_dirnames, list_filenames in elements:
            for file_name in list_filenames:
                folder = Folder(directory_path)
                file = File(folder, file_name)
                list_files.append(file)
            level += 1
            if num_levels == level:
                break

        return list_files

    def get_Folders(self, num_levels=None):
        self.is_Exist(_raise_error_on=False)

        level = 0
        list_folders = []
        elements = os.walk(self.abspath)
        for directory_path, list_dirnames, list_filenames in elements:
            for dir_name in list_dirnames:
                path = os.path.join(
                    directory_path,
                    dir_name
                )
                folder = Folder(path)
                list_folders.append(folder)
            level += 1
            if num_levels == level:
                break

        return list_folders


class File(object):
    """Objeto para el manejo de archivos.

    ATRIBUTOS:
        name = Nombre del archivo con todo y extensión.
        title = Nombre del archivo sin extensión.
        extension = Extensión del archivo.
        folder = Objeto de tipo Folder (ver definicion de la clase)
        folder_old = Objeto de tipo folder que representa el anterior
                     folder, al mover el archivo
        obj = Objecto de tipo FileObject de python.
    """

    def __init__(self, _folder, _name):
        """Constructor.

        PARAMETROS:
            _folder = Objeto de tipo Folder.
            _name = Nombre del archivo con todo y extension.
        """
        self.name = _name
        self.title = os.path.splitext(_name)[0]
        self.extension = os.path.splitext(_name)[1]
        self.folder = _folder
        self.folder_old = None
        self.obj = None

    def get_Abspath(self):
        abspath = os.path.join(
            self.folder.abspath,
            self.name
        )
        return abspath

    def is_Exist(self, _origin="", _raise_error_on=None):
        value = os.path.isfile(self.get_Abspath())
        if value:
            if _raise_error_on:
                raise Error(
                    "validacion",
                    "El archivo '%s' ya existe" % (self.get_Abspath()),
                    "archivo existe",
                    _origin,

                )
            return True
        else:
            if _raise_error_on is False:
                raise Error(
                    "validacion",
                    "El archivo '%s' no existe" % (self.get_Abspath()),
                    "archivo no existe",
                    _origin
                )
            return False

    def has_Extension(self, _extension, _raise_error_on=None):
        if self.extension.lower() == _extension.lower():
            if _raise_error_on:
                raise Error(
                    "validacion",
                    "El archivo '%s' contiene la extension '%s'" % (
                        self.name,
                        _extension
                    ),
                    "contiene extensión",
                    "",
                )
            return True
        else:
            if _raise_error_on is False:
                raise Error(
                    "validacion",
                    "El archivo '%s' no contiene la extension '%s'" % (
                        self.name,
                        _extension
                    ),
                    "no contiene extensión",
                    "",
                )
            return False

    def create(self, _overwrite=False, _raise_errors=False):
        """Metodo que crea el archivo en el sistema de archivos.

        PARAMETERS:
            _overwrite: Si se recibe True en caso de no existir el directorio o
                        el archivo, estos seran creados.

        """
        if _raise_errors:
            self.folder.is_Exist(_raise_error_on=False)
            if _overwrite is False:
                self.is_Exist(_raise_error_on=True)

            try:
                self.file_object = open(self.get_Abspath(), "w")
                print("Archivo '%s' creado con exito en '%s'" % (
                    self.name, self.folder.abspath))
                return True
            except Exception as error:
                raise Error(
                    type(error).__name__,
                    str(error),
                    "",
                    "",
                )

        else:
            try:
                self.folder.is_Exist(_raise_error_on=False)
                file_exist = self.is_Exist()
                if _overwrite is False:
                    if file_exist:
                        print("Archivo '%s' ya existe en el folder '%s'" % (
                            self.name, self.folder.abspath))
                        return False

                self.file_object = open(self.get_Abspath(), "w")
                print("Archivo '%s' creado con exito en '%s'" % (
                    self.name, self.folder.abspath))
                return True
            except Exception as error:
                print(str(error))




    # def copy(self, _folder_to, _replace=False):

    #     origin = "Archivo.copy()"

    #     self.exist(origin)

    #     carpeta_destino = _folder_to
    #     # carpeta_destino = Carpeta(_basepath_to)
    #     carpeta_destino.exist(origin)

    #     archivo_nuevo = Archivo(carpeta_destino, self.nombre)

    #     if _replace is False:
    #         archivo_nuevo.not_Exist(origin)

    #     try:
    #         shutil.copy(self.get_Abspath(), archivo_nuevo.get_Abspath())
    #         print "Se copio archivo %s al folder %s" % (
    #             archivo_nuevo.nombre,
    #             archivo_nuevo.carpeta.abspath
    #         )

    #     except Exception as error:
    #         raise Error(
    #             type(error).__name__,
    #             origin,
    #             "",
    #             str(error)
    #         )

    # def move(self, _folder_to, _replace=False):

    #     origin = "Archivo.move()"

    #     self.exist(origin)

    #     carpeta_destino = _folder_to
    #     # carpeta_destino = Carpeta(_basepath_new)
    #     carpeta_destino.exist(origin)

    #     archivo_nuevo = Archivo(carpeta_destino, self.nombre)

    #     if _replace is False:
    #         archivo_nuevo.not_Exist(origin)

    #     try:

    #         shutil.move(self.get_Abspath(), archivo_nuevo.get_Abspath())

    #         self.carpeta_old = self.carpeta
    #         self.carpeta = carpeta_destino

    #         print "Se movio archivo %s al folder %s" % (
    #             archivo_nuevo.nombre,
    #             archivo_nuevo.carpeta.abspath
    #         )

    #     except Exception as error:
    #         raise Error(
    #             type(error).__name__,
    #             origin,
    #             "",
    #             str(error)
    #         )

    # def write(self, _value):
    #     """ Metodo que permite escribir en un archivo.

    #         En caso de que no exista, crea el archivo

    #     """
    #     origin = "Archivo.write()"

    #     try:
    #         self.file_object = open(self.get_Abspath(), "wb")
    #         self.file_object.write(_value)
    #         self.file_object.close()

    #         print "Archivo %s guardado en el folder %s" % (self.nombre, self.carpeta.abspath)

    #     except Exception, error:
    #         raise Error(
    #             type(error).__name__,
    #             origin,
    #             "",
    #             str(error)
    #         )
