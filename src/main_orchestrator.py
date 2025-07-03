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

# Initialize agent bus
bus = AgentBus()

# Register core agents
eden_agent = Agent('EdenOneCity', public_key='eden_pub')
aincrad_agent = Agent('AINCRAD', public_key='aincrad_pub')
lilithos_agent = Agent('LilithOS', public_key='lilithos_pub')

eden_id = bus.register_agent(eden_agent)
aincrad_id = bus.register_agent(aincrad_agent)
lilithos_id = bus.register_agent(lilithos_agent)

# Simulate a city state update (e.g., new garden created)
zone_update = {'zone': 'Zero-G Dome', 'event': 'new_garden', 'details': {'name': 'Starlight Lotus', 'plants': 42}}
bus.send_message(sender_id=eden_id, recipient_id=aincrad_id, message={'zone_update': zone_update})

# Simulate a system event (e.g., security alert)
system_event = {'event': 'security_alert', 'level': 'critical', 'details': {'zone': 'Stargate Plaza'}}
bus.send_message(sender_id=eden_id, recipient_id=lilithos_id, message={'system_event': system_event})

# Simulate citizen input and ethical check
interface = CitizenInterface()
ethics = EthicsProtocol()

# Voice command
interface.handle_voice_input('Show me the gardens')

# Ethical check for a critical action
decision = ethics.evaluate_decision(context={'zone': 'Stargate Plaza'}, action='open_portal')
if not decision['approved']:
    ethics.request_override(user='admin', action='open_portal')

print('Live agent orchestration and data flow initialized.') 