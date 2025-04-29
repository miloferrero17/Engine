from typing import Optional, Dict
from app.Model.enums import DataType
from app.Model.base_model import BaseModel
from app.Model.field import Field
from datetime import datetime, timezone, timedelta

class Transactions(BaseModel):
    def __init__(self):
        data: Dict[str, Field] = {
            "id":           Field(None, DataType.INTEGER, False, True),  # Clave única
            "contact_id":   Field(None, DataType.INTEGER, False, False),
            "name":         Field(None, DataType.STRING, False, False),
            "phone":        Field(None, DataType.STRING, True, False),
            "conversation": Field(None, DataType.TEXT, False, False),
            "timestamp":    Field(None, DataType.TIMESTAMP, True, False)
        }
        super().__init__("transactions", data)
        self.data = data

    def add(
        self,
        contact_id: int,
        name: str,
        phone: Optional[str] = None,
        conversation: str = '',
        timestamp: Optional[str] = None
    ) -> int:
        """Agrega una nueva transacción."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        self.data["contact_id"].value = contact_id
        self.data["name"].value = name
        self.data["phone"].value = phone
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        return super().add()

    
    def get_by_contact_id(self, contact_id: int) -> Optional[Dict[str, any]]:
        """Devuelve el último registro de transacción asociado a un contact_id."""
        try:
            query = f"contact_id=eq.{contact_id}&order=timestamp.desc&limit=1"
            result = self._fetch_one(query)
            return result
        except Exception as e:
            raise DatabaseError(f"Error al obtener transacción por contact_id={contact_id}: {e}")


    def update(
        self,
        id: int,
        contact_id: Optional[int] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None,
        conversation: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> None:
        """Actualiza una transacción existente por id."""
        self.data["id"].value = id
        self.data["contact_id"].value = contact_id
        self.data["phone"].value = phone
        self.data["name"].value = name
        self.data["conversation"].value = conversation
        self.data["timestamp"].value = timestamp
        super().update("id", id)

    def delete(self, id: int) -> None:
        """Elimina una transacción por id."""
        super().delete("id", id)

    def get_last_timestamp_by_phone(self, phone: str) -> Optional[Dict[str, any]]:
        """Devuelve la última transacción (por timestamp) de un teléfono."""
        query = f"phone=eq.{phone}&order=timestamp.desc&limit=1"
        result = self._fetch_one(query)
        return result

    def get_open_conversation_by_contact_id(self, contact_id: int) -> str:
        tx = self.get_by_contact_id(contact_id)
        if tx and tx.get("name") == "Abierta":
            return tx.get("conversation") or ""
        return ""


    def get_open_transaction_id_by_contact_id(self, contact_id: int) -> Optional[int]:
        """Devuelve el id de la transacción abierta (name='Abierta') para un contact_id específico."""
        try:
            query = f"contact_id=eq.{contact_id}&name=eq.Abierta&order=timestamp.desc&limit=1"
            result = self._fetch_one(query)
            if result:
                return result.get("id")
            return None
        except Exception as e:
            raise DatabaseError(f"Error al obtener la transacción abierta para contact_id={contact_id}: {e}")
