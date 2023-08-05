# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury base parameter type definition.
"""
from werkzeug import exceptions
from werkzeug.datastructures import FileStorage
from .base import BaseProperty


class FileProperty(BaseProperty):
    """
    A File parameter definition.
    """
    flask_type = "file"

    # def __new__(cls, name, value):
    #     """
    #     A file parameter constructor.
    #     :param value: a value to be casted to int.
    #     :return: the value casted to int type
    #     """
    #
    #     if isinstance(value, io.IOBase):
    #         return value
    #     else:
    #         raise BadRequest(
    #             "Bad file received '{}'. "
    #             "We could not get the file stream, instead we got '{}'."
    #             "".format(name, value)
    #         )

    def inflate(self, value):
        value = super().inflate(value)
        if value is not None:

            if not isinstance(value, FileStorage):
                name = self.mapping_from or self.property_name
                raise exceptions.BadRequest(
                    "On property: '{}'.\n"
                    "Value: '{}'.\n"
                    "Error: A file was expected.".format(name, value)
                )

        return value

    def to_swagger(self, schema):
        """
        Swagger spec path parameter serialization function.
        :param param: function parameter pointer.
        :return: the parameter spec.
        """
        spec = super().to_swagger(schema)
        spec['type'] = 'file'
        spec['format'] = 'binary'
        spec['in'] = 'formData'

        return spec
