import logging
import pymongo
from datetime import datetime
import os
from django.conf import settings
import traceback
from time import sleep
import threading

class MongoDBHandler(logging.Handler):
    """
    Custom logging handler that stores logs in MongoDB with Docker support
    """
    
    def __init__(self, level=logging.NOTSET, max_retries=3, retry_delay=1):
        super().__init__(level)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._connection_lock = threading.Lock()
        self.setup_mongo_connection()
    
    def setup_mongo_connection(self):
        """Initialize MongoDB connection with retry logic for Docker"""
        for attempt in range(self.max_retries):
            try:
                self.mongo_uri = getattr(settings, 'MONGODB_URI', 
                                       os.getenv('MONGODB_URI', 'mongodb://mongodb:27017/django_logs'))
                self.db_name = getattr(settings, 'MONGODB_DB_NAME', 
                                     os.getenv('MONGODB_DB_NAME', 'django_logs'))
                self.collection_name = getattr(settings, 'MONGODB_LOG_COLLECTION', 
                                             os.getenv('MONGODB_LOG_COLLECTION', 'application_logs'))
                
                # Connection options for better Docker compatibility
                connection_options = {
                    'serverSelectionTimeoutMS': 5000,
                    'connectTimeoutMS': 5000,
                    'socketTimeoutMS': 5000,
                    'maxPoolSize': 50,
                    'retryWrites': True
                }
                
                self.client = pymongo.MongoClient(self.mongo_uri, **connection_options)
                
                # Test connection
                self.client.admin.command('ping')
                
                self.db = self.client[self.db_name]
                self.collection = self.db[self.collection_name]
                
                # Create indexes for better query performance
                self.create_indexes()
                
                print(f"✅ MongoDB connection established successfully (attempt {attempt + 1})")
                return
                
            except pymongo.errors.ServerSelectionTimeoutError as e:
                print(f"⚠️ MongoDB connection failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    sleep(self.retry_delay * (attempt + 1))
                else:
                    print("❌ Failed to connect to MongoDB after all retries")
                    self.client = None
            except Exception as e:
                print(f"❌ Unexpected error connecting to MongoDB: {e}")
                self.client = None
                break
    
    def create_indexes(self):
        """Create necessary indexes for log queries"""
        try:
            # TTL index for automatic log expiration (optional)
            self.collection.create_index(
                [("timestamp", pymongo.DESCENDING)], 
                background=True
            )
            self.collection.create_index(
                [("level", pymongo.ASCENDING)], 
                background=True
            )
            self.collection.create_index(
                [("logger", pymongo.ASCENDING)], 
                background=True
            )
            self.collection.create_index(
                [("module", pymongo.ASCENDING)], 
                background=True
            )
            self.collection.create_index(
                [("request.path", pymongo.ASCENDING)], 
                background=True
            )
            
            # TTL index to automatically delete logs older than 90 days
            self.collection.create_index(
                [("timestamp", pymongo.ASCENDING)], 
                expireAfterSeconds=90*24*60*60,  # 90 days
                background=True
            )
            
        except Exception as e:
            print(f"Warning: Could not create MongoDB indexes: {e}")
    
    def emit(self, record):
        """Emit a log record to MongoDB with error handling"""
        if not self.client:
            # Try to reconnect if connection was lost
            self.setup_mongo_connection()
            if not self.client:
                return
        
        try:
            log_entry = self.format_record(record)
            with self._connection_lock:
                self.collection.insert_one(log_entry)
        except pymongo.errors.ServerSelectionTimeoutError:
            print("MongoDB connection lost, attempting to reconnect...")
            self.setup_mongo_connection()
        except Exception as e:
            print(f"Failed to write log to MongoDB: {e}")
    
    def format_record(self, record):
        """Format log record for MongoDB storage"""
        
        # Handle exc_info if present
        exc_info = None
        if record.exc_info:
            exc_info = {
                'type': str(record.exc_info[0].__name__),
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        log_entry = {
            'timestamp': datetime.utcnow(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'path': record.pathname,
            'process': record.process,
            'thread': record.thread,
            'thread_name': record.threadName,
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_entry['extra_data'] = record.extra_data
        
        # Add request information if available
        if hasattr(record, 'request'):
            try:
                request = record.request
                log_entry['request'] = {
                    'method': request.method,
                    'path': request.path,
                    'user': getattr(request.user, 'username', 'anonymous') if hasattr(request, 'user') else 'anonymous',
                    'user_id': getattr(request.user, 'id', None) if hasattr(request, 'user') else None,
                    'ip_address': self.get_client_ip(request),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'query_params': dict(request.GET),
                }
            except Exception as e:
                log_entry['request_error'] = str(e)
        
        if exc_info:
            log_entry['exception'] = exc_info
        
        return log_entry
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def close(self):
        """Close MongoDB connection when handler is closed"""
        if self.client:
            self.client.close()
        super().close()