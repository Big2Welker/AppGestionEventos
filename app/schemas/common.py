from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    """Permite usar ObjectId en modelos Pydantic sin romper OpenAPI."""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        # 👇 Agregamos la validación real (llamando a validate)
        return core_schema.no_info_before_validator_function(
            cls.validate,
            core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.str_schema(),
                ],
                serialization=core_schema.plain_serializer_function_ser_schema(str),
            ),
        )

    @classmethod
    def validate(cls, v):
        """Convierte string a ObjectId o lanza error si no es válido."""
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        """Describe el tipo como string en OpenAPI."""
        json_schema = handler(schema)
        json_schema.update(type="string", example="6554a77e12f6c2f49c8e5d77")
        return json_schema

