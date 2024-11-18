from xmlrpc.client import ServerProxy

def client_transaction():
    coordinator = ServerProxy("http://localhost:8001")

    # Transaction 1: Transfer $100 from A to B
    changes = [-100, 100]  # Node-2 loses $100, Node-3 gains $100
    result = coordinator.perform_transaction(changes)
    print("Transaction 1:", result)

    # Transaction 2: Add 20% bonus to A and same amount to B
    changes = [200, 200]  # Bonus for both accounts
    result = coordinator.perform_transaction(changes)
    print("Transaction 2:", result)

# Example usage
client_transaction()
