# shared/subscribers/base_subscriber.py
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseSubscriber(ABC):
    """Base class for all event subscribers"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.subscriptions = []
    
    @abstractmethod
    def subscribe_to_events(self):
        """Subscribe to relevant events - to be implemented by subclasses"""
        pass
    
    def register_subscription(self, queue_name: str, event_type: str, callback: callable):
        """Register a subscription"""
        from shared.message_broker.event_bus import event_bus
        event_bus.subscribe(queue_name, event_type, callback)
        self.subscriptions.append({
            'queue': queue_name,
            'event_type': event_type,
            'callback': callback.__name__
        })
        logger.info(f"✅ {self.service_name} subscribed to {event_type}")
    
    def get_subscriptions(self):
        """Get list of active subscriptions"""
        return self.subscriptions