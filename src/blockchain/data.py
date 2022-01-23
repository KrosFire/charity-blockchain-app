from datetime import datetime
import pickle
import rsa


class Data():
    private_key: rsa.PrivateKey
    issuer: str
    receiver: str
    amount: int
    timestamp: str
    
    def __init__(self, private_key: rsa.PrivateKey, issuer: str, receiver: str, amount: int) -> None:
        self.private_key = private_key
        self.issuer = issuer
        self.receiver = receiver
        self.amount = amount
        self.timestamp = str(datetime.now())
    
    def hash(self) -> bytes:
        msg = (str(self)).encode()
        return rsa.sign(msg, self.private_key, 'SHA-256')
    
    def verify(self, public_key: rsa.PublicKey) -> bool:
        try:
            return rsa.verify(str(self).encode(), self.hash(), public_key) == 'SHA-256'
        except:
            return False
    
    def __str__(self) -> str:
        return f'FROM: {self.issuer}\nTO: {self.receiver}\nAMOUNT: {self.amount}\nDATE: {self.timestamp}\n'