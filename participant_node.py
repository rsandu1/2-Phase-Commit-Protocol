import sys
from xmlrpc.server import SimpleXMLRPCServer

class Participant:
    def __init__(self, account_file):
        self.account_file = account_file
        self.temp_balance = None  # Used for prepare phase

    def read_balance(self):
        """Read the current balance from the account file."""
        with open(self.account_file, 'r') as f:
            return int(f.read())

    def write_balance(self, balance):
        with open(self.account_file, 'w') as f:
            f.write(str(balance))

    def prepare(self, change):
        # if str(self.account_file) == "account_A.txt":
        #     print("Node-2: Simulating crash before responding to coordinator.")
        #     time.sleep(20)
        balance = self.read_balance()
        if balance + change >= 0:  # Check feasibility
            self.temp_balance = balance + change
            return "READY"
        else:
            return "FAIL"

    def commit(self):
        # if str(self.account_file) == "account_A.txt":
        #     print("Node-2: Simulating crash before responding to coordinator.")
        #     time.sleep(20)
        if self.temp_balance is not None:
            self.write_balance(self.temp_balance)
            self.temp_balance = None
            return "COMMITTED"

    def abort(self):
        self.temp_balance = None
        return "ABORTED"

# Start the participant RPC server
def start_participant(account_file, port):
    participant = Participant(account_file)
    server = SimpleXMLRPCServer(("localhost", port))
    server.register_instance(participant)
    print(f"Participant RPC server running on port {port}")
    server.serve_forever()

# Starting the nodes
start_participant(sys.argv[1], int(sys.argv[2]))


