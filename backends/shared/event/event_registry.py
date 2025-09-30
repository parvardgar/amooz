# shared/events/event_registry.py
from typing import Dict, Type
from shared.event.base_events import BaseEvent

class EventRegistry:
    """Registry for event types to enable deserialization"""
    
    _events: Dict[str, Type[BaseEvent]] = {}
    
    @classmethod
    def register(cls, event_class: Type[BaseEvent]):
        """Register an event class"""
        cls._events[event_class.__name__] = event_class
        return event_class
    
    @classmethod
    def get_event_class(cls, event_type: str) -> Type[BaseEvent]:
        """Get event class by type name"""
        return cls._events.get(event_type)
    
    @classmethod
    def create_event_from_dict(cls, data: Dict[str, Any]) -> BaseEvent:
        """Create event instance from dictionary"""
        event_type = data.get('event_type')
        event_class = cls.get_event_class(event_type)
        if not event_class:
            raise ValueError(f"Unknown event type: {event_type}")
        
        # Remove event_type from data as it's not a constructor parameter
        event_data = data.copy()
        event_data.pop('event_type', None)
        
        return event_class(**event_data)