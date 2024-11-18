2-Phase Commit Protocol

HOW TO RUN

Step 1: Start the Nodes
Open three terminal windows or command-line instances.

Start Participant Node for Account A (Node-2): In the first terminal, run:

python participant_node.py account_A.txt 8002

This starts the participant managing account_A.txt on port 8002.

Start Participant Node for Account B (Node-3): In the second terminal, run:

python participant_node.py account_B.txt 8003

This starts the participant managing account_B.txt on port 8003.

Start Coordinator Node (Node-1): In the third terminal, run:

python coordinator_node.py 8001

This starts the coordinator on port 8001. The coordinator knows the URLs of the participant nodes:

http://localhost:8002 for Node-2
http://localhost:8003 for Node-3

Step 2: Run the Client
Open a fourth terminal window.

Execute the client script to initiate the transactions:

python client.py
This sends the two transactions to the coordinator:

Transaction 1: Transfer $100 from Account A to Account B.
Transaction 2: Add a 20% bonus of Account A's initial balance to both accounts.