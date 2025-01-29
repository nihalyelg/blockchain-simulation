#Kept the function names pretty self-explanatory.
#Added comments wherever necessary to explain the logic.


# Importing necessary libraries
import hashlib 
import time  


class Block:
    """
    Represents a single block in the blockchain.
    """
    def __init__(self, index, transactions, previous_hash, difficulty=2):
        self.index = index  # Position of the block in the chain
        self.timestamp = int(time.time())  # Time of block creation
        self.transactions = transactions  # List of transactions in the block
        self.previous_hash = previous_hash  # Hash of the previous block
        self.nonce = 0  # Used for Proof-of-Work
        self.difficulty = difficulty  # Difficulty level for mining
        self.current_hash = self.generate_hash()  # Hash of the current block

    def generate_hash(self):
        """
        Generate the hash for the block based on its content, including the nonce for Proof-of-Work.
        """
        block_content = (
            str(self.index) + str(self.timestamp) +
            str(self.transactions) + self.previous_hash + str(self.nonce)
        )
        return hashlib.sha256(block_content.encode('utf-8')).hexdigest()

    def mine_block(self):
        """
       It performs Proof-of-Work to find a hash that meets the difficulty requirement (2) for now.
        The hash must start with a specific number of leading zeros (e.g., '00'). for the difficulty=2
        """
        start_time = time.time()
        while not self.current_hash.startswith('0' * self.difficulty):
            self.nonce += 1
            self.current_hash = self.generate_hash()
        end_time = time.time()
        print(f"Block {self.index} mined with nonce {self.nonce} in {end_time - start_time:.2f} seconds.")

    def display_block(self):
        """
        Print the details of the block in a readable format.
        """
        print(f"Block Index: {self.index}")
        print(f"Timestamp: {self.timestamp}")
        print(f"Transactions: {self.transactions}")
        print(f"Previous Hash: {self.previous_hash}")
        print(f"Current Hash: {self.current_hash}")
        print(f"Nonce: {self.nonce}")


class Blockchain:
    """
    Represents the entire blockchain as a list of blocks.
    """
    def __init__(self, difficulty=2):
        self.chain = []  # List to hold all blocks in the chain
        self.difficulty = difficulty  # Difficulty level for mining
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the blockchain, known as the genesis block.
        """
        genesis_block = Block(0, ["Genesis Block"], "0", self.difficulty)
        genesis_block.mine_block()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        """
        Add a new block to the blockchain after mining it.
        """
        previous_block = self.chain[-1]  # Get the last block in the chain
        new_block = Block(len(self.chain), transactions, previous_block.current_hash, self.difficulty)
        new_block.mine_block()
        self.chain.append(new_block)

    def validate_chain(self):
        """
        Check the validity of the blockchain by verifying the hashes and links between blocks.
        Returns True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's previous_hash matches the actual hash of the previous block
            if current_block.previous_hash != previous_block.current_hash:
                return False

            # Check if the current block's hash is still valid
            if current_block.current_hash != current_block.generate_hash():
                return False

        return True

    def tamper_block(self, index, new_transactions):
        """
        Modify the transactions of a block at a specific index to simulate tampering.
        """
        if 0 <= index < len(self.chain):  # Ensure the index is valid
            self.chain[index].transactions = new_transactions
            self.chain[index].current_hash = self.chain[index].generate_hash()  # Recalculate the hash after tampering
            print(f"Block {index} has been tampered.")
        else:
            print("Invalid block index!")

    def display_chain(self):
        """
        Display the details of every block in the blockchain.
        """
        for block in self.chain:
            print("-" * 30)
            block.display_block()


# Example usage
if __name__ == "__main__":
    # Initialize the blockchain with a mining difficulty of 3
    blockchain = Blockchain(difficulty=3)

    # Add blocks with transactions to the blockchain
    blockchain.add_block(["Alice sent 1 BTC to Bob"])
    blockchain.add_block(["Bob sent 0.5 BTC to Charlie"])
    blockchain.add_block(["Charlie sent 0.2 BTC to Dave"])

    # Display the blockchain before tampering
    print("\n--- Blockchain Before Tampering ---")
    blockchain.display_chain()

    # Validate the blockchain
    is_valid = blockchain.validate_chain()
    print(f"\nIs the blockchain valid? {is_valid}")

    # Tamper with the second block
    blockchain.tamper_block(1, ["Tampered transaction"])

    # Display the blockchain after tampering
    print("\n--- Blockchain After Tampering ---")
    blockchain.display_chain()

    # Validate the blockchain again
    is_valid = blockchain.validate_chain()
    print(f"\nIs the blockchain valid? {is_valid}")
