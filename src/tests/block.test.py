from blockchain.block import Block
import unittest


class testingBlock(unittest.TestCase):
    def test_init(self):
        index = 2
        data = 'data123' # TODO: Change to real data
        prev_hash = '123'
        nonce = 4
        
        block = Block(index, data, prev_hash, nonce)
        
        self.assertEqual(block.index, index)
        self.assertEqual(block.data, data)
        self.assertEqual(block.prev_hash, prev_hash)
        self.assertEqual(block.nonce, nonce)

    def test_string_representation(self):
        index = 2
        data = 'data123' # TODO: Change to real data
        prev_hash = '123'
        nonce = 4
        
        block = Block(index, data, prev_hash, nonce)
        
        self.assertEqual(str(block),
                         f'Block {str(index)}, nonce: {nonce} data: {str(data)}, prev_hash: {prev_hash}, hash: {block.hash()}')

if __name__ == '__main__':
    unittest.main()