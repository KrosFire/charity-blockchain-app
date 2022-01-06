from datetime import datetime
from blockchain.block import Block


class Blockchain():
    difficulty: int = 4
    
    def __init__(self, chain: list[Block] = []) -> None:
        self.chain: list[Block] = []
        if len(chain) == 0:
           genesisBlock = Block()
           self.mine(genesisBlock)
           chain.append(genesisBlock)
        
        self.chain = chain[:]
    
    def add(self, block: Block) -> None:
        self.chain.append(block)
    
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
    
    def __str__(self) -> str:
        res = ""
        for block in self.chain:
            res += str(block)
            
        return res