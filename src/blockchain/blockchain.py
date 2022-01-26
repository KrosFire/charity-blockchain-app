from datetime import datetime
import pickle
from markupsafe import re

import rsa
from blockchain.data import Data
from blockchain.block import Block
from database.db_setup import Database

class Blockchain():
    difficulty: int = 4
    
    def __init__(self, mock: bool = False) -> None:
        self.mock = mock
        bc_col = Database().get_blockchain_collection()
        bc = bc_col.find_one() if not mock else None
        if bc != None:
            self.chain = [pickle.loads(el) for el in pickle.loads(bytes(bc['chain'], 'latin1'))]
        else:
            self.chain: list[Block] = []
        if len(self.chain) == 0:
           genesisBlock = Block()
           self.mine(genesisBlock)
        
        if not mock and bc == None:
            bc_col.insert_one({ '_id': 'main_blockchain',
                               'chain': str(
                                   pickle.dumps([pickle.dumps(block) for block in self.chain]),
                                   encoding="latin1") })

    def add(self, block: Block) -> None:
        self.chain.append(block)
        bc_col = Database().get_blockchain_collection()
        if not self.mock and bc_col.find_one({ '_id': 'main_blockchain' }):
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
            # print(private_key)
            formatted_key = rsa.PrivateKey.load_pkcs1(private_key.encode())
            # print(formatted_key)
            new_block = Block(
                len(self.chain)+1,
                Data(
                    formatted_key,
                    'ID-BANK',
                    id,
                    100
                ))
            self.mine(new_block)
            return True
        return False
    
    def make_donation(self, issuer: str, amount: int, private_key: str) -> tuple[bool, str]:
        users_col = Database().get_users_collection()
        receiver = 'ID-CHARITY'
        
        if self.get_user_balance(issuer) < amount:
            return False, 'Insufficient funds'
        
        issuer_data = users_col.find_one({ '_id': issuer })
        pub_key = rsa.PublicKey.load_pkcs1(issuer_data['public_key'].encode())
        
        if issuer_data == None:
            return False, 'Issuer not found'
        
        formatted_key: rsa.PrivateKey
        try:
            formatted_key = rsa.PrivateKey.load_pkcs1(private_key.encode())
        except:
            print('Formatting is wrong')
            return False, 'Invalid private key'
        
        transaction = Data(formatted_key, issuer, receiver, amount)
        
        if not transaction.verify(pub_key):
            print('Data verification failed')
            return False, 'Invalid private key'
        
        block = Block(len(self.chain)+1, transaction)
        self.mine(block)
        return True, 'Transaction successfull'
    
    def get_user_balance(self, id) -> int:
        balance = 0
        for block in self.chain:
            if block.data != None:
                if block.data.receiver == id:
                    balance += block.data.amount
                elif block.data.issuer == id:
                    balance -= block.data.amount
                    
        return balance
    
    def list_transactions(self) -> list[str]:
        res = []
        for block in self.chain:
            if block.data == None:
                continue
            issuer_id = block.data.issuer
            receiver_id = block.data.receiver
            amount = block.data.amount
            date = block.data.timestamp
            
            print(block.data)
            
            user_col = Database().get_users_collection()
            issuer = user_col.find_one({ '_id': issuer_id })
            receiver = user_col.find_one({ '_id': receiver_id })
            
            res.append(f'FROM: { issuer["name"] } TO: { receiver["name"] } AMOUNT: { amount } DATE: { date }')

        return res
    def __str__(self) -> str:
        res = ""
        for block in self.chain:
            if len(res) > 0:
                res += "|\n|\n\\/\n"
            res += str(block)
            
        return res
