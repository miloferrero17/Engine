from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field

class Transactions(BaseModel):
    def __init__(self):
        # Definición de campos, incluyendo id como clave única y event_id tipo SMALLINT (int2)
        fields: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),
            "event_id": Field(None, DataType.INTEGER, True, False),  # int2 / SMALLINT
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False),
            "puntuacion": Field(None, DataType.INTEGER, True, False),  # int2 / SMALLINT
            "comentario": Field(None, DataType.STRING, True, False),    # text
            "data_created": Field(None, DataType.TIMESTAMP, False, False)  # timestamp de creación
        }
        super().__init__("transactions", fields)
        # Exponer los campos para facilitar su uso
        self.data = self._BaseModel__data

    def add(
        self,
        contact_id: int,
        phone: str,
        name: Optional[str] = None,
        conversation: str = "",
        timestamp: Optional[str] = None,
        event_id: Optional[int] = None,
        puntuacion: Optional[int] = None,
        comentario: Optional[str] = None,
        data_created: Optional[str] = None
    ) -> int:
        # Inicializa el id en None para auto-incrementar
        self.data["id"].value = None
        self.data["event_id"].value = event_id
        self.data["contact_id"].value = contact_id
        self.data["phone"].value = phone
        self.data["name"].value = name
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        self.data["puntuacion"].value = puntuacion
        self.data["comentario"].value = comentario
        self.data["data_created"].value = data_created
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        results = super().get("id", id, order_field="timestamp")
        return results[0] if results else None

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp,
            "name": last.name
        }

    def get_by_contact_id(self, contact_id: int) -> List[TransactionsRegister]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> List[TransactionsRegister]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transactions = self.get_by_contact_id(contact_id)
        for tx in transactions:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transactions = self.get_by_contact_id(contact_id)
        abiertas = [tx for tx in transactions if tx.name == "Abierta"]
        return abiertas[-1].id if abiertas else None

    def get_event_id_by_tx_id(self, tx_id: int) -> Optional[int]:
        """
        Retorna el event_id asociado a una transacción dada su id.
        """
        tx = self.get_by_id(tx_id)
        return tx.event_id if tx and tx.event_id is not None else None

    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None,
        event_id: Optional[int] = None,
        puntuacion: Optional[int] = None,
        comentario: Optional[str] = None
    ) -> None:
        # Establecer id para la clave única
        self.data["id"].value = id
        # Actualiza solo los campos proporcionados
        if event_id is not None:
            self.data["event_id"].value = event_id
        if contact_id is not None:
            self.data["contact_id"].value = contact_id
        if phone is not None:
            self.data["phone"].value = phone
        if name is not None:
            self.data["name"].value = name
        if conversation is not None:
            self.data["conversation"].value = conversation
        if timestamp is not None:
            self.data["timestamp"].value = timestamp
        if puntuacion is not None:
            self.data["puntuacion"].value = puntuacion
        if comentario is not None:
            self.data["comentario"].value = comentario
        # Llama a la actualización usando 'id' como clave única
        super().update("id", id)

    def delete(self, id: int) -> None:
        super().delete("id", id)

    def get_last_transaction_by_event_and_phone(
        self, event_id: int, phone: str
    ) -> Optional[TransactionsRegister]:
        """
        Retorna la última transacción asociada a un event_id y un teléfono dado,
        o None si no existe.
        """
        # Primero traemos todas las txs de ese teléfono ordenadas por timestamp
        txs_por_telf = super().get("phone", phone, order_field="timestamp")
        # Filtramos sólo las que tengan el event_id buscado
        txs_filtradas = [tx for tx in txs_por_telf if tx.event_id == event_id]
        # Devolvemos la última (más reciente) o None
        return txs_filtradas[-1] if txs_filtradas else None

    def get_conversation_by_id(self, tx_id) -> str:
        """
        Devuelve el JSON de `conversation` de la transacción con id = tx_id,
        o cadena vacía si no existe o está vacío.
        Acepta `tx_id` int o str.
        """
        try:
            tx_id_int = int(tx_id)
        except (ValueError, TypeError):
            return ""

        tx = self.get_by_id(tx_id_int)
        return tx.conversation or ""

'''
from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field

class Transactions(BaseModel):
    def __init__(self):
        # Definición de campos, incluyendo id como clave única y event_id tipo SMALLINT (int2)
        fields: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),
            "event_id": Field(None, DataType.INTEGER, True, False),  # int2 / SMALLINT
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", fields)
        # Exponer los campos para facilitar su uso
        self.data = self._BaseModel__data

    def add(
        self,
        contact_id: int,
        phone: str,
        name: Optional[str] = None,
        conversation: str = "",
        timestamp: Optional[str] = None,
        event_id: Optional[int] = None
    ) -> int:
        # Inicializa el id en None para auto-incrementar
        self.data["id"].value = None
        self.data["event_id"].value = event_id
        self.data["contact_id"].value = contact_id
        self.data["phone"].value = phone
        self.data["name"].value = name
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        results = super().get("id", id, order_field="timestamp")
        return results[0] if results else None

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp,
            "name": last.name
        }

    def get_by_contact_id(self, contact_id: int) -> List[TransactionsRegister]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> List[TransactionsRegister]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transactions = self.get_by_contact_id(contact_id)
        for tx in transactions:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transactions = self.get_by_contact_id(contact_id)
        abiertas = [tx for tx in transactions if tx.name == "Abierta"]
        return abiertas[-1].id if abiertas else None

    def get_event_id_by_tx_id(self, tx_id: int) -> Optional[int]:
        """
        Retorna el event_id asociado a una transacción dada su id.
        """
        tx = self.get_by_id(tx_id)
        return tx.event_id if tx and tx.event_id is not None else None

    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None,
        event_id: Optional[int] = None
    ) -> None:
        # Establecer id para la clave única
        self.data["id"].value = id
        # Actualiza solo los campos proporcionados
        if event_id is not None:
            self.data["event_id"].value = event_id
        if contact_id is not None:
            self.data["contact_id"].value = contact_id
        if phone is not None:
            self.data["phone"].value = phone
        if name is not None:
            self.data["name"].value = name
        if conversation is not None:
            self.data["conversation"].value = conversation
        if timestamp is not None:
            self.data["timestamp"].value = timestamp
        # Llama a la actualización usando 'id' como clave única
        super().update("id", id)

    def delete(self, id: int) -> None:
        super().delete("id", id)


    def get_last_transaction_by_event_and_phone(
            self, event_id: int, phone: str
        ) -> Optional[TransactionsRegister]:
            """
            Retorna la última transacción asociada a un event_id y un teléfono dado,
            o None si no existe.
            """
            # Primero traemos todas las txs de ese teléfono ordenadas por timestamp
            txs_por_telf = super().get("phone", phone, order_field="timestamp")
            # Filtramos sólo las que tengan el event_id buscado
            txs_filtradas = [tx for tx in txs_por_telf if tx.event_id == event_id]
            # Devolvemos la última (más reciente) o None
            return txs_filtradas[-1] if txs_filtradas else None
    
    def get_conversation_by_id(self, tx_id) -> str:
        """
        Devuelve el JSON de `conversation` de la transacción con id = tx_id,
        o cadena vacía si no existe o está vacío.
        Acepta `tx_id` int o str.
        """
        try:
            tx_id_int = int(tx_id)
        except (ValueError, TypeError):
            return ""

        tx = self.get_by_id(tx_id_int)
        return tx.conversation or ""
    

tx = Transactions()
evento = 3
telefono = "5491133585362"

last_tx = tx.get_last_transaction_by_event_and_phone(evento, telefono)
if last_tx:
    print(f"Encontré tx id={last_tx.id} para event={evento} y teléfono={telefono}")
else:
    print(f"No hay transacción para event={evento} y teléfono={telefono}")



from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field

class Transactions(BaseModel):
    def __init__(self):
        # Definición de campos, incluyendo id como clave única
        fields: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", fields)
        # Exponer los campos para facilitar su uso
        self.data = self._BaseModel__data

    def add(
        self,
        contact_id: int,
        phone: str,
        name: Optional[str] = None,
        conversation: str = "",
        timestamp: Optional[str] = None
    ) -> int:
        # Inicializa el id en None para auto-incrementar
        self.data["id"].value = None
        self.data["contact_id"].value = contact_id
        self.data["phone"].value = phone
        self.data["name"].value = name
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        results = super().get("id", id, order_field="timestamp")
        return results[0] if results else None

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp,
            "name": last.name  # 👈 agregamos esto
        }

    def get_by_contact_id(self, contact_id: int) -> List[TransactionsRegister]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> List[TransactionsRegister]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transactions = self.get_by_contact_id(contact_id)
        for tx in transactions:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transactions = self.get_by_contact_id(contact_id)
        abiertas = [tx for tx in transactions if tx.name == "Abierta"]
        return abiertas[-1].id if abiertas else None

    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> None:
        # Establecer id para la clave única
        self.data["id"].value = id
        # Actualiza solo los campos proporcionados
        if contact_id is not None:
            self.data["contact_id"].value = contact_id
        if phone is not None:
            self.data["phone"].value = phone
        if name is not None:
            self.data["name"].value = name
        if conversation is not None:
            self.data["conversation"].value = conversation
        if timestamp is not None:
            self.data["timestamp"].value = timestamp
        # Llama a la actualización usando 'id' como clave única
        super().update("id", id)

    def delete(self, id: int) -> None:
        super().delete("id", id)



from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field
from app.Model.contacts import Contacts

class Transactions(BaseModel):
    def __init__(self):
        data: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),  # 👈 Clave única
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", data)
        self.__data = self._BaseModel__data  # 👈 Arreglo para que funcione el update
        self.data = self.__data  # 👈 Para comodidad tuya si querés usar data manualmente

    def add(
        self,
        contact_id: int,
        phone: str,
        name: Optional[str] = None,
        conversation: str = '',
        timestamp: Optional[str] = None
    ) -> int:
        self.__data["id"].value = None
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        return super().get("id", id, order_field="timestamp")[0]

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp
        }

    def get_by_contact_id(self, contact_id: int) -> Optional[List[TransactionsRegister]]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> Optional[List[TransactionsRegister]]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return ""
        for tx in transacciones:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return None
        abiertas = [tx for tx in transacciones if tx.name == "Abierta"]
        if not abiertas:
            return None
        return abiertas[-1].id

    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> None:
        self.__data["id"].value = id
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        super().update("id", id)

    def delete(self, id: int) -> None:
        super().delete("id", id)

from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field
from app.Model.contacts import Contacts

class Transactions(BaseModel):
    def __init__(self):
        data: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),  # 👈 Clave única
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", data)
        self.data = self._BaseModel__data  # 👈 Acceso de conveniencia si querés usar data a mano

    def add(
        self,
        contact_id: int,
        phone: str,
        name: Optional[str] = None,
        conversation: str = '',
        timestamp: Optional[str] = None
    ) -> int:
        self.__data["id"].value = None
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        return super().get("id", id, order_field="timestamp")[0]

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp
        }

    def get_by_contact_id(self, contact_id: int) -> Optional[List[TransactionsRegister]]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> Optional[List[TransactionsRegister]]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return ""
        for tx in transacciones:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return None
        abiertas = [tx for tx in transacciones if tx.name == "Abierta"]
        if not abiertas:
            return None
        return abiertas[-1].id

    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> None:
        self.__data["id"].value = id
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        super().update("id", id)

    def delete(self, id: int) -> None:
        super().delete("id", id)

from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field
from app.Model.contacts import Contacts

class Transactions(BaseModel):
    def __init__(self):
        data: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", data)
        self.data = self._BaseModel__data  # 👈 así accedés al __data privado de BaseModel correctamente

        
    def __init__(self):
        data: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),  # 👈 Clave única
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        #super().__init__("transactions", data)  # ✅ Este es el constructor que tenías comentado
        #self.data = data  # ✅ OK para compatibilidad
        self.__data = data  # 👈 asegurás que __data existe, que es el que usa BaseModel
    

    def add(
        self,
        contact_id: int,
        phone: str,
        name: Optional[str] = None,
        conversation: str = '',
        timestamp: Optional[str] = None
    ) -> int:
        self.data["id"].value = None
        self.data["contact_id"].value = contact_id
        self.data["phone"].value = phone
        self.data["name"].value = name
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        return super().get("id", id, order_field="timestamp")[0]

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp
        }

    def get_by_contact_id(self, contact_id: int) -> Optional[List[TransactionsRegister]]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> Optional[List[TransactionsRegister]]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return ""
        for tx in transacciones:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return None
        abiertas = [tx for tx in transacciones if tx.name == "Abierta"]
        if not abiertas:
            return None
        return abiertas[-1].id

    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> None:
        self.data["id"].value = id
        self.data["contact_id"].value = contact_id
        self.data["phone"].value = phone
        self.data["name"].value = name
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        super().update("id", id)  # ✅ Este es el nombre correcto del campo UNIQUE

    def delete(self, id: int) -> None:
        super().delete("id", id)



# transactions.py

from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field
from app.Model.contacts import Contacts

class Transactions(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "id": Field(None, DataType.INTEGER, False, True),  # 👈 ¡CAMBIO CLAVE!
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", self.__data)
        self.data = self.__data

    def add(self, contact_id: int, phone: str, name: Optional[str] = None, conversation: str = '', timestamp: Optional[str] = None) -> int:
        self.__data["id"].value = None
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, id: int) -> Optional[TransactionsRegister]:
        return super().get("id", id, order_field="timestamp")[0]

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None
        last = results[-1]
        return {
            "id": last.id,
            "timestamp": last.timestamp
        }

    def get_by_contact_id(self, contact_id: int) -> Optional[List[TransactionsRegister]]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> Optional[List[TransactionsRegister]]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return ""
        for tx in transacciones:
            if tx.name == "Abierta":
                return tx.conversation or ""
        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return None
        abiertas = [tx for tx in transacciones if tx.name == "Abierta"]
        if not abiertas:
            return None
        return abiertas[-1].id

    def update(self, id: int, contact_id: Optional[int] = None, phone: Optional[str] = None,
            name: Optional[str] = None, conversation: Optional[str] = None, timestamp: Optional[str] = None) -> None:
        self.__data["id"].value = id  # 👈 ESTO ES LO CRÍTICO

        # Asignar el resto
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp

        # Hacer update usando el campo único 'id'
        super().update("id", id)

    def delete(self, id: int) -> None:
        super().delete("id", id)




# transactions.py

from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field
from app.Model.contacts import Contacts

class Transactions(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "_id": Field(None, DataType.INTEGER, False, True),
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "phone": Field(None, DataType.STRING, True, False),  # Campo obligatorio agregado
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        super().__init__("transactions", self.__data)
        self.data = self.__data

    def add(self, contact_id: int, phone: str, name: Optional[str] = None, conversation: str = '', timestamp: Optional[str] = None) -> int:
        """
        Inserta un nuevo registro de transacción y devuelve su ID.
        """
        self.__data["_id"].value = None
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        return super().add()

    def get_by_id(self, _id: int) -> Optional[TransactionsRegister]:
        return super().get("_id", _id, order_field="timestamp")[0]

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, str]]:
        """
        Devuelve el timestamp y el ID de la última conversación registrada para un número de teléfono específico.
        """
        results = super().get("phone", phone, order_field="timestamp")
        if not results:
            return None

        last = results[-1]  # Suponiendo que están ordenados ascendente
        return {
            "id": last._id,
            "timestamp": last.timestamp
        }


    
    def get_by_contact_id(self, contact_id: int) -> Optional[List[TransactionsRegister]]:
        return super().get("contact_id", contact_id, order_field="timestamp")

    def get_by_name(self, name: str) -> Optional[List[TransactionsRegister]]:
        return super().get("name", name, order_field="timestamp")

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        """
        Devuelve el campo 'conversation' de la transacción abierta (name='Abierta')
        para un contact_id dado. Si no existe, devuelve string vacío.
        """
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return ""

        for tx in transacciones:
            if tx.name == "Abierta":
                return tx.conversation or ""

        return ""

    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        """
        Devuelve el ID de la última transacción con name = 'Abierta' para el contact_id dado.
        Si no existe, devuelve None.
        """
        transacciones = self.get_by_contact_id(contact_id)
        if not transacciones:
            return None

        # Filtramos solo las abiertas
        abiertas = [tx for tx in transacciones if tx.name == "Abierta"]

        if not abiertas:
            return None

        # Retornamos el ID de la más reciente (última de la lista)
        return abiertas[-1]._id

    def update(self, _id: int, contact_id: Optional[int] = None, phone: Optional[str] = None,
               name: Optional[str] = None, conversation: Optional[str] = None, timestamp: Optional[str] = None) -> None:
        self.__data["_id"].value = _id
        self.__data["contact_id"].value = contact_id
        self.__data["phone"].value = phone
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        super().update("_id", _id)

    def delete(self, _id: int) -> None:
        super().delete("_id", _id)


# transactions.py

from typing import Optional, List, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel, TransactionsRegister
from app.Model.field import Field

class Transactions(BaseModel):
    def __init__(self):
        self.__data: Dict[str, Field] = {
            "_id": Field(None, DataType.INTEGER, False, True),
            "contact_id": Field(None, DataType.INTEGER, False, False),
            "name": Field(None, DataType.STRING, False, False),
            "conversation": Field(None, DataType.STRING, False, False),
            "timestamp": Field(None, DataType.TIMESTAMP, False, False)
        }
        # Se pasa el nombre de la tabla y el diccionario de campos a BaseModel.
        super().__init__("transactions", self.__data)
        # Si necesitas acceder a la estructura de datos fuera del constructor, la asignas a un atributo.
        self.data = self.__data

    def add(self, contact_id: int, name: Optional[str] = None, conversation: str = '', timestamp: Optional[str] = None) -> int:
        """
        Inserta un nuevo registro de transacción y devuelve su ID.
        """
        self.__data["_id"].value = None
        self.__data["contact_id"].value = contact_id
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        return super().add()

# Instanciación sin pasar DatabaseManager
#go = Transactions()
#go.add(28)
    def get_by_id(self, _id: int) -> Optional[TransactionsRegister]:
        """
        Returns an instance of TransactionsRegister with the data of the transaction identified by _id.
        """
        result = super().get("_id", _id, order_field="timestamp")
        return result[0] if result else None

    def get_by_contact_id(self, contact_id: int) -> Optional[List[TransactionsRegister]]:
        """
        Returns a list of TransactionsRegister instances for records with the given contact_id.
        """
        return super().get("contact_id", contact_id, order_field="timestamp")



    def get_by_name(self, name: str) -> Optional[List[TransactionsRegister]]:
            """
            Returns a list of TransactionsRegister instances for records matching the given name.
            """
            return super().get("name", name, order_field="timestamp")
    


    def update(self, _id: int, contact_id: Optional[int] = None, name: Optional[str] = None, conversation: Optional[str] = None, timestamp: Optional[str] = None) -> None:
        """
        Updates the data of a transaction identified by _id.
        Only fields with non-None values will be updated.
        """
        self.__data["_id"].value = _id
        self.__data["contact_id"].value = contact_id
        self.__data["name"].value = name
        self.__data["conversation"].value = conversation
        self.__data["timestamp"].value = timestamp
        super().update("_id", _id)
    

    def delete(self, _id: int) -> None:
        """
        Deletes the transaction identified by _id.
        """
        super().delete("_id", _id)
'''