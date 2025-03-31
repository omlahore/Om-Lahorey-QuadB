from flask import Flask, request, jsonify
import hashlib
import time
import json

# -------------------- Block Class --------------------
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

# -------------------- Blockchain Class --------------------
class Blockchain:
    difficulty = 3

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, ["Genesis Block"], time.time(), "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, transactions):
        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          transactions=transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

    def print_chain(self):
        print("\n=== Blockchain Contents ===")
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Transactions: {block.transactions}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Current Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("-" * 50)

    def tamper_with_block(self, index, fake_data):
        if 0 < index < len(self.chain):
            self.chain[index].transactions = [fake_data]
            print(f"⚠️ Tampered with block at index {index}!")
        else:
            print("❌ Invalid index to tamper with.")

# -------------------- Flask App Setup --------------------
app = Flask(__name__)
blockchain = Blockchain()

# Print the chain when the app starts
blockchain.print_chain()

# -------------------- Routes --------------------

# 📦 Get full blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    return jsonify(chain_data), 200

# 🧱 Add new block
@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.get_json()
    transactions = data.get("transactions", [])
    if not transactions:
        return jsonify({"error": "No transactions provided"}), 400
    blockchain.add_block(transactions)
    return jsonify({"message": "Block added"}), 201

# ✅ Validate blockchain
@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({"valid": is_valid}), 200

# 🧪 Tamper with blockchain (demo)
@app.route('/tamper', methods=['POST'])
def tamper_chain():
    data = request.get_json()
    index = data.get("index")
    fake_data = data.get("fake_data", "Tampered Transaction")
    if index is None:
        return jsonify({"error": "No block index provided"}), 400
    blockchain.tamper_with_block(index, fake_data)
    return jsonify({"message": f"Block {index} has been tampered with."}), 200

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
