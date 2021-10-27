
import hashlib
import json
import datetime

class Transaction:
    def __init__(self, sender : str, reciever : str, amount: float) -> None:
        self.sender = sender
        self.reciver = reciever
        self.amount = amount
        self.timestamp = datetime.datetime.now()

    def __str__(self) -> str:
        return f"{self.sender} sent {self.amount} amount to {self.reciver} at {self.timestamp}."
    
    def calc_hash(self) -> str:
        encoded = str(self).encode()
        return hashlib.sha256(encoded).hexdigest()

class Block:
    def __init__(self, timestamp:datetime, transactions : list[Transaction], previous_hash : str) -> None:
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calc_hash()
        

    def __str__(self) -> str:
        return f"{self.transactions} {self.previous_hash} {self.timestamp} {self.nonce}"

    def calc_hash(self) -> str:
        encoded = str(self).encode()
        return hashlib.sha256(encoded).hexdigest()

    def mine(self, difficulty : int) -> str:
        while(self.calc_hash()[:difficulty] != "0"*difficulty):
            self.nonce += 1

        print("New block has been mined!!!")

        self.hash = self.calc_hash()

        return self.hash

class BlockChain:
    def __init__(self, difficulty : int) -> None:
        timestamp = datetime.datetime.now()
        genesis_block = Block(timestamp, [], "0"*difficulty)
        genesis_block.hash = "0"*difficulty
        self.difficulty = difficulty
        self.chain = [genesis_block]
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, new_block) -> None:
        self.chain.append(new_block)

    def __str__(self) -> str:
        return_str = ""
        block_count = 1

        for block in self.chain:
            return_str += f"\nBLOCK No:{block_count}\nPREVIOUS HASH:\n{block.previous_hash[:20]}\n"
            return_str +=  "TRANSACTIONS\n"
            trans_count = 1
            for trans in block.transactions:
                return_str += f"{trans_count}. {trans}\n"
                trans_count += 1
            return_str += f"HASH:\n{block.hash[:20]}\n" + "="*50 + "\n\n"
            block_count += 1
        return return_str

if __name__ == "__main__":
    
    difficulty = 5
    BC = BlockChain(difficulty)
    mempool = open("mempool.json","r")
    new_transactions = json.load(mempool)

    for t in new_transactions:
        trans = Transaction(t["sender"], t["reciever"], t["amount"])
        
        latest_block = BC.get_latest_block()
        all_transactions = latest_block.transactions.copy()
        previous_hash = latest_block.hash
        all_transactions.append(trans)

        new_block = Block(trans.timestamp, all_transactions, previous_hash)
        new_block.mine(BC.difficulty)
        BC.add_block(new_block)

    print(BC)