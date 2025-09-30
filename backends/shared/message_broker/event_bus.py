# shared/message_broker/event_bus.py
import logging
import time
from typing import Callable
from shared.message_broker.rabbitmq import rabbitmq_broker
from shared.event.event_registry import EventRegistry

logger = logging.getLogger(__name__)

class EventBus:
    """Enhanced event bus with better control"""
    
    def __init__(self):
        self.broker = rabbitmq_broker
        self._running = False
        self._setup_infrastructure()
    
    def _setup_infrastructure(self):
        """Setup required exchanges and queues"""
        self.broker.declare_exchange('domain_events', 'topic', durable=True)
        self.broker.declare_exchange('dlx.domain_events', 'topic', durable=True)
        self.broker.declare_queue('dlq.domain_events', durable=True)
        self.broker.bind_queue('dlx.domain_events', 'dlq.domain_events', '#')
    
    def publish(self, event, routing_key: str = None) -> bool:
        """Publish a domain event"""
        if not routing_key:
            routing_key = event.event_type.lower()
        
        message = event.to_dict()
        
        success = self.broker.publish(
            exchange='domain_events',
            routing_key=routing_key,
            message=message
        )
        
        if success:
            logger.info(f"📤 Published event: {event.event_type}")
        return success
    
    def subscribe(self, queue_name: str, event_type: str, callback: Callable, durable: bool = True) -> None:
        """Subscribe to events"""
        self.broker.declare_queue(queue_name, durable=durable)
        routing_key = event_type.lower()
        self.broker.bind_queue('domain_events', queue_name, routing_key)
        
        def message_handler(message):
            try:
                event = EventRegistry.create_event_from_dict(message)
                logger.info(f"🔄 Processing event: {event.event_type}")
                callback(event)
            except Exception as e:
                logger.error(f"❌ Failed to process event: {e}")
                raise
        
        self.broker.consume(queue_name, message_handler, auto_ack=False)
        logger.info(f"📥 Subscribed to {event_type} on queue {queue_name}")
    
    def start(self):
        """Start consuming events"""
        if self._running:
            logger.warning("⚠️ Event bus already running")
            return
        
        self._running = True
        logger.info("🔄 Starting event bus...")
        self.broker.start_consuming()
    
    def stop(self):
        """Stop consuming events"""
        if not self._running:
            return
        
        self._running = False
        logger.info("⏹️ Stopping event bus...")
        self.broker.stop_consuming()
    
    def health_check(self):
        """Health check"""
        return {
            'running': self._running,
            'rabbitmq_connected': self.broker.health_check()
        }

event_bus = EventBus()