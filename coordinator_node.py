from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

class Coordinator:
    def __init__(self, participants):
        self.participants = participants  # List of participant RPC URLs

    def query_balance(self, participant_url):
        """Query the current balance of a participant."""
        proxy = ServerProxy(participant_url)
        return proxy.read_balance()

    def perform_transaction(self, changes):
        # Phase 1: Prepare
        results = []
        for participant, change in zip(self.participants, changes):
            proxy = ServerProxy(participant)
            try:
                result = proxy.prepare(change)
                results.append(result)
            except Exception:
                results.append("FAIL")  # Treat errors as failure

        # Check if all participants are ready
        if all(res == "READY" for res in results):
            # Phase 2: Commit
            for participant in self.participants:
                proxy = ServerProxy(participant)
                try:
                    proxy.commit()
                except Exception:
                    print(f"Error committing to {participant}")
            return "Transaction Committed"
        else:
            # Abort if any participant fails
            for participant in self.participants:
                proxy = ServerProxy(participant)
                try:
                    proxy.abort()
                except Exception:
                    print(f"Error aborting at {participant}")
            return "Transaction Aborted"

# Start the coordinator RPC server
def start_coordinator(participants, port):
    coordinator = Coordinator(participants)
    server = SimpleXMLRPCServer(("localhost", port))
    server.register_instance(coordinator)
    server.register_function(coordinator.query_balance, "query_balance")
    print(f"Coordinator RPC server running on port {port}")
    server.serve_forever()

# Example usage
if __name__ == "__main__":
    participants = ["http://localhost:8002", "http://localhost:8003"]
    start_coordinator(participants, 8001)
