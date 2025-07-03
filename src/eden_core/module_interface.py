"""
Eden One City - EdenModuleInterface

Quantum-detailed interface for all plug-and-play system modules.

📋 QUANTUM DOCUMENTATION:
- Defines the standard interface for all core modules (engines) in Eden One City.
- Ensures plug-and-play compatibility, dynamic loading/unloading, and unified system orchestration.
- All modules must implement this interface for system integration.

🧩 FEATURE CONTEXT:
- Enables modular, scalable, and adaptive architecture.
- Supports multi-agent AI, real-time data flow, and secure co-governance.

🧷 DEPENDENCY LISTINGS:
- Used by all core engines (cultural, emotional, creature, memory, portal, environment).
- Required for agent communication and system orchestration layers.

💡 USAGE EXAMPLES:
- class MyEngine(EdenModuleInterface): ...
- engine = MyEngine(); engine.register(context); engine.process(data); engine.shutdown()

⚡ PERFORMANCE CONSIDERATIONS:
- Interface is lightweight and designed for high-frequency, low-latency calls.

🔒 SECURITY IMPLICATIONS:
- All module actions are subject to system-level access control and audit logging.

📜 CHANGELOG:
- 2024-06-19: Interface created for Eden One City plug-and-play refactor.
"""

from abc import ABC, abstractmethod

class EdenModuleInterface(ABC):
    """
    Abstract base class for all Eden One City plug-and-play modules.
    """
    @abstractmethod
    def register(self, system_context):
        """
        Register the module with the system context.
        Args:
            system_context (dict): Shared system resources and configuration.
        Returns:
            bool: Success status.
        """
        pass

    @abstractmethod
    def process(self, input_data):
        """
        Process input data and return output.
        Args:
            input_data (dict): Data to process.
        Returns:
            dict: Output data/results.
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Cleanly shut down the module, releasing resources.
        Returns:
            bool: Success status.
        """
        pass 