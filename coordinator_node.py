from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

class Coordinator:
    def __init__(self, participants):
        self.participants = participants  # List of participant RPC URLs

    def perform_transaction(self, changes):
        # Phase 1: Prepare
        results = []
        for participant, change in zip(self.participants, changes):
            proxy = ServerProxy(participant)
            result = proxy.prepare(change)
            results.append(result)
        
        # Check if all participants are ready
        if all(res == "READY" for res in results):
            # Phase 2: Commit
            for participant in self.participants:
                proxy = ServerProxy(participant)
                proxy.commit()
            return "Transaction Committed"
        else:
            # Abort if any participant fails
            for participant in self.participants:
                proxy = ServerProxy(participant)
                proxy.abort()
            return "Transaction Aborted"

# Start the coordinator RPC server
def start_coordinator(participants, port):
    coordinator = Coordinator(participants)
    server = SimpleXMLRPCServer(("localhost", port))
    server.register_instance(coordinator)
    print(f"Coordinator RPC server running on port {port}")
    server.serve_forever()

# Example usage for Coordinator Node
participants = ["http://localhost:8002", "http://localhost:8003"]
start_coordinator(participants, 8001)
