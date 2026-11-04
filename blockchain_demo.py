import hashlib
import json
from datetime import datetime, timezone


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Combine all important block information
        block_contents = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }

        # Convert block information into consistent JSON
        encoded_data = json.dumps(
            block_contents,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

        # Generate SHA-256 hash
        return hashlib.sha256(encoded_data).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []

        # Create the first block
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            0,
            {"message": "Blockchain initialized"},
            "0" * 64
        )

        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )

        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(len(self.chain)):

            current_block = self.chain[i]

            # Check whether the block's contents still match its hash
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check whether the block points to the correct previous block
            if i > 0:
                previous_block = self.chain[i - 1]

                if current_block.previous_hash != previous_block.hash:
                    return False

        return True

    def display_chain(self):
        for block in self.chain:
            print("\n------------------------------")
            print("Block Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Block Hash:", block.hash)


# ---------------------------------
# MAIN PROGRAM
# ---------------------------------

my_blockchain = Blockchain()

# Add a medication record
my_blockchain.add_block({
    "patient_ref": "PAT-DEMO-001",
    "medication": "Metformin",
    "status": "Taken"
})

# Add an AI prediction record
my_blockchain.add_block({
    "patient_ref": "PAT-DEMO-001",
    "prediction": "Low Adherence Risk",
    "confidence": 0.92
})

print("\n========== ORIGINAL BLOCKCHAIN ==========")

my_blockchain.display_chain()

print("\nIs blockchain valid?", my_blockchain.is_chain_valid())


# ---------------------------------
# TAMPERING EXPERIMENT
# ---------------------------------

print("\n========== TAMPERING EXPERIMENT ==========")

# Change the medication status in Block 1
my_blockchain.chain[1].data["status"] = "Missed"

print("\nSomeone changed Block 1's medication status!")

print("Is blockchain valid after tampering?",
      my_blockchain.is_chain_valid())
# ---------------------------------
# REHASHING EXPERIMENT
# ---------------------------------

print("\n========== REHASHING EXPERIMENT ==========")

# Recalculate Block 1's hash after tampering
my_blockchain.chain[1].hash = (
    my_blockchain.chain[1].calculate_hash()
)

print("\nBlock 1's hash has been recalculated!")

print("Is blockchain valid after rehashing Block 1?",
      my_blockchain.is_chain_valid())
# ---------------------------------
# ENTIRE CHAIN REBUILD EXPERIMENT
# ---------------------------------

print("\n========== ENTIRE CHAIN REBUILD ==========")

# Recalculate every block after the genesis block
for i in range(1, len(my_blockchain.chain)):
    current_block = my_blockchain.chain[i]
    previous_block = my_blockchain.chain[i - 1]

    # Update the link to the previous block
    current_block.previous_hash = previous_block.hash

    # Recalculate the current block's hash
    current_block.hash = current_block.calculate_hash()

print("\nAttacker recalculated all subsequent blocks!")

print("Is blockchain valid after rebuilding?",
      my_blockchain.is_chain_valid())