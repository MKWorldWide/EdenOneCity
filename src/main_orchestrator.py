"""
Eden One City - Main Orchestrator

📋 QUANTUM DOCUMENTATION:
- Bootstraps the multi-agent system for Eden One City, AINCRAD, and LilithOS.
- Registers all agents, sets up the agent bus, and demonstrates real data flow.
- Example: City state update routed to AINCRAD for visualization, system event sent to LilithOS.

🧩 FEATURE CONTEXT:
- Enables live, modular orchestration and real-time data flow between all core systems.

💡 USAGE EXAMPLE:
$ python src/main_orchestrator.py
"""

import time
from src.eden_core.agent_bus import AgentBus, Agent
from src.eden_core.citizen_interface import CitizenInterface
from src.eden_core.ethics_protocol import EthicsProtocol
from src.eden_core.aincrad_integration import send_zone_update, listen_for_aincrad_events
from src.eden_core.lilithos_integration import log_system_event, register_service, listen_for_lilithos_events

# Initialize agent bus
bus = AgentBus()

# Register core agents
eden_agent = Agent('EdenOneCity', public_key='eden_pub')
aincrad_agent = Agent('AINCRAD', public_key='aincrad_pub')
lilithos_agent = Agent('LilithOS', public_key='lilithos_pub')

eden_id = bus.register_agent(eden_agent)
aincrad_id = bus.register_agent(aincrad_agent)
lilithos_id = bus.register_agent(lilithos_agent)

# Register additional agents
maintenance_bot = Agent('MaintenanceBot', public_key='maint_pub')
event_coordinator = Agent('EventCoordinator', public_key='event_pub')
security_ai = Agent('SecurityAI', public_key='sec_pub')

maint_id = bus.register_agent(maintenance_bot)
event_id = bus.register_agent(event_coordinator)
sec_id = bus.register_agent(security_ai)

# Register EdenOneCity as a service with LilithOS
register_service({'service': 'EdenOneCity', 'type': 'city_module'})

# Send a real zone update to AINCRAD
send_zone_update({'zone': 'Zero-G Dome', 'event': 'new_garden', 'details': {'name': 'Starlight Lotus', 'plants': 42}})

# Log a real system event to LilithOS
log_system_event({'event': 'security_alert', 'level': 'critical', 'details': {'zone': 'Stargate Plaza'}})

# Feedback loop: Listen for AINCRAD and LilithOS events

def on_aincrad_event(event):
    print(f'[Orchestrator] Received AINCRAD event: {event}')
    # Example: Forward visualization confirmation to EdenOneCity agent
    bus.send_message(sender_id=aincrad_id, recipient_id=eden_id, message={'visualization_feedback': event})

def on_lilithos_event(event):
    print(f'[Orchestrator] Received LilithOS event: {event}')
    # Example: Forward resource update to MaintenanceBot
    bus.send_message(sender_id=lilithos_id, recipient_id=maint_id, message={'resource_update': event})

listen_for_aincrad_events(on_aincrad_event)
listen_for_lilithos_events(on_lilithos_event)

print('Advanced agent orchestration, real API integration, and feedback loops initialized.') 