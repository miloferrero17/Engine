from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, MessagesRegister
from app.Model.field import Field

class Messages(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "message_id":    Field(None, DataType.INTEGER, False, True),
            "msg_key":       Field(None, DataType.INTEGER, False, False),
            "text":          Field(None, DataType.STRING,  False, False),
            "phone":         Field(None, DataType.STRING,  True,  False),  # opcional
            "question_id":   Field(None, DataType.INTEGER, True,  False),  # FK opcional
            "group_id":      Field(None, DataType.INTEGER, True,  False),  # FK opcional
            "question_name": Field(None, DataType.STRING,  True,  False)   # ✅ Nuevo campo opcional
        }
        super().__init__("messages", self.__data)

    def add(
        self,
        msg_key:       int,
        text:          str,
        phone:         Optional[str] = None,
        question_id:   Optional[int] = None,
        group_id:      Optional[int] = None,
        question_name: Optional[str] = None
    ) -> int:
        """
        Inserta un nuevo mensaje y retorna su ID.
        Los campos phone, question_id, group_id y question_name son opcionales.
        """
        self.__data["message_id"].value    = None
        self.__data["msg_key"].value       = msg_key
        self.__data["text"].value          = text
        self.__data["phone"].value         = phone
        self.__data["question_id"].value   = question_id
        self.__data["group_id"].value      = group_id
        self.__data["question_name"].value = question_name
        return super().add()

    def get_last_group_id_by_phone(self, phone: str) -> Optional[int]:
        """
        Obtiene el group_id del último mensaje enviado desde un número de teléfono dado.
        """
        last_message = self.get_latest_by_phone(phone)

        if last_message and last_message.group_id is not None:
            return last_message.group_id
        else:
            return None

    def get_by_phone(self, phone: str) -> Optional[List[MessagesRegister]]:
        """
        Returns messages associated with a specific phone number.
        """
        return super().get("phone", phone)

    def get_latest_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the most recent message (by highest message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados:
            return max(resultados, key=lambda r: r.message_id)
        return None

    def get_penultimate_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the second most recent message (by message_id) for a specific phone.
        """ 
        resultados = super().get("phone", phone)
        if resultados and len(resultados) >= 2:
            resultados_ordenados = sorted(resultados, key=lambda r: r.message_id, reverse=True)
            return resultados_ordenados[1]
        return None

    def get_by_id(self, message_id: int) -> Optional[MessagesRegister]:
        """
        Retorna una instancia de MessagesRegister con los datos del mensaje identificado por message_id.
        """
        result = super().get("message_id", message_id)
        return result[0] if result else None

    def get_penultimate_question_id_by_phone(self, phone: str) -> Optional[int]:
        """
        Retorna el question_id del penúltimo mensaje asociado a un número de teléfono.
        """
        penultimo_mensaje = self.get_penultimate_by_phone(phone)
        if penultimo_mensaje and penultimo_mensaje.question_id is not None:
            return penultimo_mensaje.question_id
        return None

    def update(
        self,
        message_id:    int,
        msg_key:       Optional[int] = None,
        text:          Optional[str] = None,
        phone:         Optional[str] = None,
        question_id:   Optional[int] = None,
        group_id:      Optional[int] = None,
        question_name: Optional[str] = None
    ) -> None:
        """
        Actualiza los datos de un mensaje identificado por message_id.
        Solo se actualizan los campos cuyo valor no sea None.
        """
        self.__data["message_id"].value = message_id
        if msg_key is not None:
            self.__data["msg_key"].value = msg_key
        if text is not None:
            self.__data["text"].value = text
        if phone is not None:
            self.__data["phone"].value = phone
        if question_id is not None:
            self.__data["question_id"].value = question_id
        if group_id is not None:
            self.__data["group_id"].value = group_id
        if question_name is not None:
            self.__data["question_name"].value = question_name

        super().update("message_id", message_id)

    def delete(self, message_id: int) -> None:
        """
        Elimina el mensaje identificado por message_id.
        """
        super().delete("message_id", message_id)

'''
from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, MessagesRegister
from app.Model.field import Field

class Messages(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "message_id":  Field(None, DataType.INTEGER, False, True),
            "msg_key":     Field(None, DataType.INTEGER, False, False),
            "text":        Field(None, DataType.STRING,  False, False),
            "phone":       Field(None, DataType.STRING,  True,  False),  # opcional
            "question_id": Field(None, DataType.INTEGER, True,  False),  # FK opcional
            "group_id":    Field(None, DataType.INTEGER, True,  False),  # FK opcional
        }
        super().__init__("messages", self.__data)

    def add(
        self,
        msg_key:     int,
        text:        str,
        phone:       Optional[str] = None,
        question_id: Optional[int] = None,
        group_id:    Optional[int] = None
    ) -> int:
        """
        Inserta un nuevo mensaje y retorna su ID.
        Los campos phone, question_id y group_id son opcionales.
        """
        self.__data["message_id"].value  = None
        self.__data["msg_key"].value     = msg_key
        self.__data["text"].value        = text
        self.__data["phone"].value       = phone
        self.__data["question_id"].value = question_id
        self.__data["group_id"].value    = group_id
        return super().add()

    def get_by_phone(self, phone: str) -> Optional[List[MessagesRegister]]:
        """
        Returns messages associated with a specific phone number.
        """
        return super().get("phone", phone)

    def get_latest_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the most recent message (by highest message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados:
            return max(resultados, key=lambda r: r.message_id)
        return None

    def get_penultimate_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the second most recent message (by message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados and len(resultados) >= 2:
            resultados_ordenados = sorted(resultados, key=lambda r: r.message_id, reverse=True)
            return resultados_ordenados[1]
        return None

    def get_by_id(self, message_id: int) -> Optional[MessagesRegister]:
        """
        Retorna una instancia de MessagesRegister con los datos del mensaje identificado por message_id.
        """
        result = super().get("message_id", message_id)
        return result[0] if result else None

    def update(
        self,
        message_id:  int,
        msg_key:     Optional[int] = None,
        text:        Optional[str] = None,
        phone:       Optional[str] = None,
        question_id: Optional[int] = None,
        group_id:    Optional[int] = None
    ) -> None:
        """
        Actualiza los datos de un mensaje identificado por message_id.
        Solo se actualizan los campos cuyo valor no sea None.
        """
        self.__data["message_id"].value = message_id
        if msg_key is not None:
            self.__data["msg_key"].value = msg_key
        if text is not None:
            self.__data["text"].value = text
        if phone is not None:
            self.__data["phone"].value = phone
        if question_id is not None:
            self.__data["question_id"].value = question_id
        if group_id is not None:
            self.__data["group_id"].value = group_id

        super().update("message_id", message_id)

    def delete(self, message_id: int) -> None:
        """
        Elimina el mensaje identificado por message_id.
        """
        super().delete("message_id", message_id)

from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, MessagesRegister
from app.Model.field import Field


class Messages(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "message_id":  Field(None, DataType.INTEGER, False, True),
            "msg_key":     Field(None, DataType.INTEGER, False, False),
            "text":        Field(None, DataType.STRING,  False, False),
            "phone":       Field(None, DataType.STRING,  True,  False),  # opcional
            "question_id": Field(None, DataType.INTEGER, True,  False),  # nueva columna FK opcional
        }
        super().__init__("messages", self.__data)

    def add(
        self,
        msg_key:     int,
        text:        str,
        phone:       Optional[str] = None,
        question_id: Optional[int] = None
    ) -> int:
        """
        Inserta un nuevo mensaje y retorna su ID.
        Los campos phone y question_id son opcionales.
        """
        self.__data["message_id"].value  = None
        self.__data["msg_key"].value     = msg_key
        self.__data["text"].value        = text
        self.__data["phone"].value       = phone
        self.__data["question_id"].value = question_id
        return super().add()

    def get_by_phone(self, phone: str) -> Optional[List[MessagesRegister]]:
        """
        Returns messages associated with a specific phone number.
        """
        return super().get("phone", phone)

    def get_latest_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the most recent message (by highest message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados:
            return max(resultados, key=lambda r: r.message_id)
        return None

    def get_penultimate_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the second most recent message (by message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados and len(resultados) >= 2:
            resultados_ordenados = sorted(resultados, key=lambda r: r.message_id, reverse=True)
            return resultados_ordenados[1]
        return None

    def get_by_id(self, message_id: int) -> Optional[MessagesRegister]:
        """
        Retorna una instancia de MessagesRegister con los datos del mensaje identificado por message_id.
        """
        result = super().get("message_id", message_id)
        return result[0] if result else None

    def update(
        self,
        message_id:  int,
        msg_key:     Optional[int] = None,
        text:        Optional[str] = None,
        phone:       Optional[str] = None,
        question_id: Optional[int] = None
    ) -> None:
        """
        Actualiza los datos de un mensaje identificado por message_id.
        Solo se actualizan los campos cuyo valor no sea None.
        """
        self.__data["message_id"].value = message_id
        if msg_key is not None:
            self.__data["msg_key"].value     = msg_key
        if text is not None:
            self.__data["text"].value        = text
        if phone is not None:
            self.__data["phone"].value       = phone
        if question_id is not None:
            self.__data["question_id"].value = question_id

        super().update("message_id", message_id)

    def delete(self, message_id: int) -> None:
        """
        Elimina el mensaje identificado por message_id.
        """
        super().delete("message_id", message_id)


from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, MessagesRegister
from app.Model.field import Field


class Messages(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "message_id": Field(None, DataType.INTEGER, False, True),
            "msg_key": Field(None, DataType.INTEGER, False, False),
            "text": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False)  # ✅ ahora es opcional (nullable=True)
        }
        super().__init__("messages", self.__data)

    def add(self, msg_key: int, text: str, phone: Optional[str] = None) -> int:
        """
        Inserta un nuevo mensaje y retorna su ID. El campo phone es opcional.
        """
        self.__data["message_id"].value = None
        self.__data["msg_key"].value = msg_key
        self.__data["text"].value = text
        self.__data["phone"].value = phone
        return super().add()




    def get_by_phone(self, phone: str) -> Optional[List[MessagesRegister]]:
        """
        Returns messages associated with a specific phone number.
        """
        return super().get("phone", phone)



    def get_latest_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the most recent message (by highest message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados:
            return max(resultados, key=lambda r: r.message_id)
        return None

    def get_penultimate_by_phone(self, phone: str) -> Optional[MessagesRegister]:
        """
        Returns the second most recent message (by message_id) for a specific phone.
        """
        resultados = super().get("phone", phone)
        if resultados and len(resultados) >= 2:
            # Ordenamos los resultados por message_id de forma descendente
            resultados_ordenados = sorted(resultados, key=lambda r: r.message_id, reverse=True)
            return resultados_ordenados[1]  # El segundo más reciente
        return None

    def get_by_id(self, message_id: int) -> Optional[MessagesRegister]:
        """
        Retorna una instancia de MessagesRegister con los datos del mensaje identificado por message_id.
        """
        result = super().get("message_id", message_id)
        return result[0] if result else None


    def update(
        self,
        message_id: int,
        msg_key: Optional[int] = None,
        text: Optional[str] = None,
        phone: Optional[str] = None
    ) -> None:
        """
        Actualiza los datos de un mensaje identificado por message_id.
        Solo se actualizan los campos cuyo valor no sea None.
        """
        self.__data["message_id"].value = message_id
        if msg_key is not None:
            self.__data["msg_key"].value = msg_key
        if text is not None:
            self.__data["text"].value = text
        if phone is not None:
            self.__data["phone"].value = phone
        super().update("message_id", message_id)
        
    def delete(self, message_id: int) -> None:
        """
        Elimina el mensaje identificado por message_id.
        """
        super().delete("message_id", message_id)
'''