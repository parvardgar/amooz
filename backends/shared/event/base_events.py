# shared/events/base_events.py
import uuid
from abc import ABC
from typing import Any, Dict
from django.utils import timezone
from dataclasses import dataclass, asdict
import json

@dataclass
class BaseEvent(ABC):
    """Base class for all events with serialization support"""
    event_id: str
    event_type: str
    timestamp: str
    version: int = 1
    
    def __init__(self, **kwargs):
        self.event_id = str(uuid.uuid4())
        self.event_type = self.__class__.__name__
        self.timestamp = timezone.now().isoformat()
        self.version = 1
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Serialize event to JSON"""
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize event from JSON"""
        data = json.loads(json_str)
        event_type = data.pop('event_type')
        return cls(**data)

@dataclass
class DomainEvent(BaseEvent):
    """Domain events with business context"""
    aggregate_id: str = None
    correlation_id: str = None
    
    def __init__(self, aggregate_id: str = None, correlation_id: str = None, **kwargs):
        super().__init__(**kwargs)
        self.aggregate_id = aggregate_id
        self.correlation_id = correlation_id or str(uuid.uuid4())