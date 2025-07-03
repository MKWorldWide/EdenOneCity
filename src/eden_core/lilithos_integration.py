"""
Eden One City - LilithOS Integration

📋 QUANTUM DOCUMENTATION:
- Provides functions to register services and send system events to LilithOS.
- Uses REST API for event logging and service registration.

💡 USAGE EXAMPLE:
from src.eden_core.lilithos_integration import log_system_event, register_service, listen_for_lilithos_events
register_service({'service': 'EdenOneCity', 'type': 'city_module'})
log_system_event({'event': 'security_alert', 'level': 'critical', 'details': {...}})
listen_for_lilithos_events(on_event_callback)
"""

import requests
import threading
import time

LILITHOS_API_URL = 'http://localhost:9000/api/system_event'  # Update as needed
LILITHOS_SERVICE_URL = 'http://localhost:9000/api/register_service'  # Update as needed
LILITHOS_WS_URL = 'ws://localhost:9000/ws/events'  # Update as needed


def register_service(service_data):
    """Register a service with LilithOS via REST API."""
    try:
        response = requests.post(LILITHOS_SERVICE_URL, json=service_data)
        print(f'[LilithOS Integration] Registered service: {service_data}, Response: {response.status_code}')
        return response.json()
    except Exception as e:
        print(f'[LilithOS Integration] Error registering service: {e}')
        return {'status': 'error', 'message': str(e)}


def log_system_event(event):
    """Log a system event to LilithOS via REST API."""
    try:
        response = requests.post(LILITHOS_API_URL, json=event)
        print(f'[LilithOS Integration] Logged system event: {event}, Response: {response.status_code}')
        return response.json()
    except Exception as e:
        print(f'[LilithOS Integration] Error logging system event: {e}')
        return {'status': 'error', 'message': str(e)}


def listen_for_lilithos_events(callback):
    """Stub for listening to LilithOS events via WebSocket (to be implemented if supported)."""
    def _listen():
        print('[LilithOS Integration] Listening for LilithOS events (stub)...')
        # Example: Simulate receiving events
        while True:
            time.sleep(15)
            event = {'event': 'resource_update', 'details': {'service': 'EdenOneCity', 'status': 'healthy'}}
            callback(event)
    thread = threading.Thread(target=_listen, daemon=True)
    thread.start() 