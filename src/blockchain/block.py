from datetime import datetime
from blockchain.data import Data
from hashlib import sha256


class Block():    
    def __init__(
        self,
        index: int = 1,
        data: Data = None,
        prev_hash: str = "0"*64,
        nonce: int = 0) -> None:
        
        self.data = data
        self.index = index
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.timestamp = str(datetime.now())
    
    def hash(self) -> str:
        h = sha256()
        to_digest = str(self.nonce ** 2) + self.prev_hash + str(self.index ** 2) + str(self.data)
        h.update(to_digest.encode('utf-8'))
        return h.hexdigest()
    
    def __str__(self) -> str:
        return (f"Block {self.index}\n" +
                f"nonce: {self.nonce}\n" +
                f"data: {str(self.data)}\n" +
                f"prev_hash: {self.prev_hash}\n" +
                f"hash: {self.hash()}\n")
