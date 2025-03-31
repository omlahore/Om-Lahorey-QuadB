from flask import Flask, request, jsonify, render_template, redirect, url_for
import hashlib
import time
import json
from threading import Lock

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
        """
        Returns the hash of the block instance by converting its contents into a JSON string and hashing it.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

# -------------------- Blockchain Class --------------------
class Blockchain:
    difficulty = 3

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.lock = Lock()
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates the genesis block and appends it to the chain.
        The genesis block has an index of 0 and a previous_hash of "0".
        """
        genesis_block = Block(0, ["Genesis Block"], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Returns the last block in the chain.
        """
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Simple Proof of Work Algorithm:
        - Increment the nonce value until the hash of the block starts with a number of zeros equal to the difficulty level.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        """
        Adds a block to the chain after verification.
        Verification includes:
        - Checking if the previous_hash referred in the block matches the hash of the latest block in the chain.
        - Validating the proof of work.
        """
        previous_hash = self.get_last_block().hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Validates the Proof: Checks if the block_hash starts with the required number of zeros (difficulty level)
        and matches the computed hash of the block.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        """
        Adds a new transaction to the list of pending transactions.
        """
        self.pending_transactions.append(transaction)

    def mine(self):
        """
        Mines a new block by adding pending transactions to the blockchain.
        This function uses a lock to ensure thread safety.
        """
        with self.lock:
            if not self.pending_transactions:
                return False
            last_block = self.get_last_block()
            new_block = Block(index=last_block.index + 1,
                              transactions=self.pending_transactions,
                              timestamp=time.time(),
                              previous_hash=last_block.hash)
            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)
            self.pending_transactions = []
            return new_block

    def is_chain_valid(self):
        """
        Checks the validity of the blockchain by ensuring that each block's hash is valid
        and that each block's previous_hash matches the hash of the preceding block.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

# -------------------- Flask App Setup --------------------
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    """
    Renders the homepage with the current blockchain data.
    """
    chain_data = [block.__dict__ for block in blockchain.chain]
    return render_template('index.html', chain=chain_data)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """
    Handles the addition of new transactions.
    On GET request, renders the transaction form.
    On POST request, adds the transaction to the pending transactions and redirects to the homepage.
    """
    if request.method == 'POST':
        transaction_data = request.form['transaction']
        blockchain.add_new_transaction(transaction_data)
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

@app.route('/mine', methods=['GET'])
def mine():
    """
    Mines a new block if there are pending transactions and redirects to the homepage.
    """
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return redirect(url_for('index'))

@app.route('/validate', methods=['GET'])
def validate():
    """
    Validates the blockchain and renders the validation result.
    """
    is_valid = blockchain.is_chain_valid()
    return render_template('validate.html', valid=is_valid)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
