# shared/message_broker/rabbitmq_broker.py
import pika
import json
import logging
import uuid
from typing import Callable, Dict, Any, Optional
from threading import Lock
from shared.utils.singleton import SingletonMeta

logger = logging.getLogger(__name__)

class RabbitMQBroker(metaclass=SingletonMeta):
    """Singleton RabbitMQ broker for event-driven communication"""
    
    def __init__(self, 
                 host: str = 'localhost',
                 port: int = 5672,
                 username: str = 'guest',
                 password: str = 'guest',
                 virtual_host: str = '/'):
        
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=pika.PlainCredentials(username, password),
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
        self._consuming_channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
        self._lock = Lock()
        self._is_connected = False
        
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to RabbitMQ with retry logic"""
        try:
            with self._lock:
                if self._connection and not self._connection.is_closed:
                    return
                
                self._connection = pika.BlockingConnection(self.connection_params)
                self._channel = self._connection.channel()
                self._consuming_channel = self._connection.channel()
                
                # Configure quality of service
                self._channel.basic_qos(prefetch_count=1)
                self._consuming_channel.basic_qos(prefetch_count=1)
                
                self._is_connected = True
                logger.info("Successfully connected to RabbitMQ")
                
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self._is_connected = False
            raise
    
    def _ensure_connection(self) -> None:
        """Ensure connection is alive, reconnect if necessary"""
        if not self._is_connected or self._connection.is_closed:
            logger.warning("RabbitMQ connection lost, reconnecting...")
            self._connect()
    
    def declare_exchange(self, exchange_name: str, exchange_type: str = 'topic', durable: bool = True) -> None:
        """Declare an exchange"""
        self._ensure_connection()
        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            durable=durable
        )
    
    def declare_queue(self, queue_name: str, durable: bool = True, **kwargs) -> None:
        """Declare a queue"""
        self._ensure_connection()
        self._channel.queue_declare(
            queue=queue_name,
            durable=durable,
            **kwargs
        )
    
    def bind_queue(self, exchange: str, queue: str, routing_key: str) -> None:
        """Bind queue to exchange with routing key"""
        self._ensure_connection()
        self._channel.queue_bind(
            exchange=exchange,
            queue=queue,
            routing_key=routing_key
        )
    
    def publish_event(self, 
                     exchange: str, 
                     routing_key: str, 
                     event_type: str,
                     data: Dict[str, Any],
                      correlation_id: Optional[str] = None) -> None:
        """
        Publish an event to RabbitMQ
        """
        self._ensure_connection()
        
        event = {
            'event_id': str(uuid.uuid4()),
            'event_type': event_type,
            'timestamp': self._get_current_timestamp(),
            'correlation_id': correlation_id or str(uuid.uuid4()),
            'data': data
        }
        
        try:
            self._channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(event, default=str),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Persistent message
                    content_type='application/json',
                    correlation_id=event['correlation_id']
                )
            )
            logger.info(f"Published event {event_type} to {routing_key}")
            
        except Exception as e:
            logger.error(f"Failed to publish event {event_type}: {e}")
            self._reconnect()
            raise
    
    def subscribe_event(self, 
                       queue: str, 
                       event_type: str, 
                       callback: Callable[[Dict[str, Any]], None],
                       auto_ack: bool = False) -> None:
        """
        Subscribe to events on a specific queue
        """
        self._ensure_connection()
        
        def message_callback(ch, method, properties, body):
            try:
                message = json.loads(body.decode())
                
                if message.get('event_type') == event_type:
                    logger.info(f"Processing event {event_type} from queue {queue}")
                    callback(message)
                
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode message: {e}")
                if not auto_ack:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                if not auto_ack:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        
        self._consuming_channel.basic_consume(
            queue=queue,
            on_message_callback=message_callback,
            auto_ack=auto_ack
        )
    
    def start_consuming(self) -> None:
        """Start consuming messages"""
        self._ensure_connection()
        logger.info("Starting event consumption...")
        self._consuming_channel.start_consuming()
    
    def stop_consuming(self) -> None:
        """Stop consuming messages"""
        if self._consuming_channel and self._consuming_channel.is_open:
            self._consuming_channel.stop_consuming()
    
    def close_connection(self) -> None:
        """Close RabbitMQ connection"""
        with self._lock:
            try:
                if self._channel and self._channel.is_open:
                    self._channel.close()
                if self._consuming_channel and self._consuming_channel.is_open:
                    self._consuming_channel.close()
                if self._connection and self._connection.is_open:
                    self._connection.close()
                
                self._is_connected = False
                logger.info("RabbitMQ connection closed")
                
            except Exception as e:
                logger.error(f"Error closing RabbitMQ connection: {e}")
    
    def _reconnect(self) -> None:
        """Reconnect to RabbitMQ"""
        self.close_connection()
        self._connect()
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from django.utils import timezone
        return timezone.now().isoformat()
    
    def __del__(self):
        """Destructor to ensure proper cleanup"""
        self.close_connection()


# Global broker instance
event_broker = RabbitMQBroker()