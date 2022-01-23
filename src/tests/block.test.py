import pickle
from blockchain.block import Block
import unittest
from blockchain.data import Data


class testingBlock(unittest.TestCase):
    def test_init(self):
        index = 2
        data = Data('some_private_key', 'issuer', 'receiver', 420)
        prev_hash = '123'
        nonce = 4
        
        block = Block(index, data, prev_hash, nonce)
        
        self.assertEqual(block.index, index)
        self.assertEqual(block.data, data)
        self.assertEqual(block.prev_hash, prev_hash)
        self.assertEqual(block.nonce, nonce)

    def test_string_representation(self):
        index = 2
        data = Data('some_private_key', 'issuer', 'receiver', 420)
        prev_hash = '123'
        nonce = 4
        
        block = Block(index, data, prev_hash, nonce)
        
        self.assertEqual(str(block),
                         f'Block {str(index)}\nnonce: {nonce}\ndata: {str(data)}\nprev_hash: {prev_hash}\nhash: {block.hash()}\n')
    def test_eval_of_serialized_data(self):
        index = 2
        data = Data('some_private_key', 'issuer', 'receiver', 420)
        prev_hash = '123'
        nonce = 4
        
        block = Block(index, data, prev_hash, nonce)
        
        ser_block = pickle.dumps(block)
        copy_block = pickle.loads(ser_block)
        
        self.assertEqual(block.index, copy_block.index)
        self.assertEqual(block.data.amount, copy_block.data.amount)
        self.assertEqual(block.data.issuer, copy_block.data.issuer)
        self.assertEqual(block.data.receiver, copy_block.data.receiver)
        self.assertEqual(block.data.private_key, copy_block.data.private_key)
        self.assertEqual(block.data.timestamp, copy_block.data.timestamp)
        self.assertEqual(block.prev_hash, copy_block.prev_hash)
        self.assertEqual(block.nonce, copy_block.nonce)


if __name__ == '__main__':
    unittest.main()