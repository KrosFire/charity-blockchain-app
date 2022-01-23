from datetime import datetime
import pickle

import rsa
from blockchain.block import Block
from database.db_setup import Database

class Blockchain():
    difficulty: int = 4
    
    def __init__(self) -> None:
        bc_col = Database().get_blockchain_collection()
        bc = bc_col.find_one()
        if bc != None:
            print(bc)
            bc_from_db = [pickle.loads(el) for el in pickle.loads(bytes(bc['chain'], 'latin1'))]
            print([str(el) for el in bc_from_db])
        self.chain: list[Block] = []
        if len(self.chain) == 0:
           genesisBlock = Block()
           self.mine(genesisBlock)
        
        if bc == None:
            bc_col.insert_one({ '_id': 'main_blockchain',
                               'chain': str(
                                   pickle.dumps([pickle.dumps(block) for block in self.chain]),
                                   encoding="latin1") })

    def add(self, block: Block) -> None:
        self.chain.append(block)
        bc_col = Database().get_blockchain_collection()
        if bc_col.find_one({ '_id': 'main_blockchain' }):
            bc_col.update_one({ '_id': 'main_blockchain' },
                            { '$set': {
                                'chain': str(
                                    pickle.dumps([pickle.dumps(block) for block in self.chain]),
                                    encoding="latin1")
                                }
                            })
    
    def mine(self, block: Block) -> None:
        try:
            block.prev_hash = self.chain[-1].hash()
        except IndexError:
            pass
        
        block.index = len(self.chain)+1
        while True:
            if block.hash()[0:self.difficulty] == "0"*self.difficulty:
                block.timestamp = str(datetime.now())
                self.add(block)
                break
            else:
                block.nonce += 1
    
    def is_valid(self) -> bool:
        # Verify genesis block
        genesisBlock = self.chain[0]
        
        if (genesisBlock.prev_hash != "0"*64 or
            genesisBlock.hash()[0:self.difficulty] != "0"*self.difficulty or
            genesisBlock.index != 1):
            return False

        for i in range(1, len(self.chain)):
            prev_block = self.chain[i-1]
            block = self.chain[i]
            
            if (prev_block.hash() != block.prev_hash or
                block.hash()[0:self.difficulty] != "0"*self.difficulty or
                block.index != i+1 or
                block.timestamp < prev_block.timestamp):
                return False
        return True
    
    def give_user_ct(self, id) -> bool:
        users_col = Database().get_users_collection()
        bank = users_col.find_one({ '_id': 'ID-BANK' })
        if bank != None:
            private_key = bank['private_key']
            print(private_key)
            formatted_key = rsa.PrivateKey().load_pkcs1(private_key.encode())
            print(formatted_key)
            # new_block = Block(
            #     len(self.chain)+1,
            #     Data())
        return False
    
    def __str__(self) -> str:
        res = ""
        for block in self.chain:
            res += str(block)
            
        return res

if __name__ == '__main__':
    bc = Blockchain()