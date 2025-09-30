# shared/message_broker/rpc_client.py
import pika
import json
import uuid
import logging
from typing import Dict, Any, Optional
from shared.utils.singleton import SingletonMeta

logger = logging.getLogger(__name__)

class RPCClient(metaclass=SingletonMeta):
    """Singleton RPC client for synchronous service communication"""
    
    def __init__(self, 
                 host: str = 'localhost',
                 port: int = 5672,
                 username: str = 'guest', 
                 password: str = 'guest'):
        
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username, password)
        )
        
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
        self._response_queue: Optional[str] = None
        self._correlation_map: Dict[str, Any] = {}
        self._connect()
    
    def _connect(self) -> None:
        """Establish RPC connection"""
        try:
            self._connection = pika.BlockingConnection(self.connection_params)
            self._channel = self._connection.channel()
            
            # Declare exclusive callback queue for responses
            result = self._channel.queue_declare(queue='', exclusive=True)
            self._response_queue = result.method.queue
            
            self._channel.basic_consume(
                queue=self._response_queue,
                on_message_callback=self._on_response,
                auto_ack=True
            )
            
            logger.info("RPC client connected successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect RPC client: {e}")
            raise
    
    def _on_response(self, ch, method, props, body):
        """Handle RPC responses"""
        if props.correlation_id in self._correlation_map:
            self._correlation_map[props.correlation_id] = json.loads(body.decode())
    
    def call(self, 
             service: str, 
             method: str, 
             params: Dict[str, Any],
             timeout: int = 30) -> Dict[str, Any]:
        """
        Make RPC call to another service
        """
        if not self._channel or self._channel.is_closed:
            self._connect()
        
        correlation_id = str(uuid.uuid4())
        self._correlation_map[correlation_id] = None
        
        request = {
            'service': service,
            'method': method,
            'params': params,
            'correlation_id': correlation_id
        }
        
        try:
            self._channel.basic_publish(
                exchange='',
                routing_key=f'rpc_{service}',
                properties=pika.BasicProperties(
                    reply_to=self._response_queue,
                    correlation_id=correlation_id,
                ),
                body=json.dumps(request)
            )
            
            # Wait for response with timeout
            import time
            start_time = time.time()
            while self._correlation_map[correlation_id] is None:
                self._connection.process_data_events(time_limit=1)
                if time.time() - start_time > timeout:
                    raise TimeoutError(f"RPC call to {service}.{method} timed out")
            
            response = self._correlation_map.pop(correlation_id)
            
            if response.get('error'):
                raise RPCException(response['error'])
                
            return response.get('result')
            
        except Exception as e:
            logger.error(f"RPC call failed: {e}")
            self._correlation_map.pop(correlation_id, None)
            raise
    
    def close(self):
        """Close RPC connection"""
        try:
            if self._channel and self._channel.is_open:
                self._channel.close()
            if self._connection and self._connection.is_open:
                self._connection.close()
        except Exception as e:
            logger.error(f"Error closing RPC connection: {e}")


class RPCException(Exception):
    """Custom exception for RPC errors"""
    pass


# Global RPC client instance
rpc_client = RPCClient()