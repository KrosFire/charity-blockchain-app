from unittest import mock
from blockchain.blockchain import Blockchain, Block, Database
import unittest


class testingBlockchain(unittest.TestCase):      
        
    def test_init(self):
        bc = Blockchain(True)
        
        self.assertEqual(len(bc.chain), 1)
        
        genesisBlock = bc.chain[0]
        
        self.assertEqual(genesisBlock.hash()[0:bc.difficulty], "0" * bc.difficulty)
        self.assertEqual(genesisBlock.prev_hash, "0" * 64)
        self.assertEqual(genesisBlock.data, None)

    def test_adding_block(self):
        block = Block(True)
        
        bc = Blockchain()
        
        bc.add(block)
        
        self.assertEqual(bc.chain[-1], block)
    
    def test_block_mining(self):
        bc = Blockchain(True)
        block = Block(2, prev_hash=bc.chain[-1])
        
        bc.mine(block)
        
        self.assertEqual(block.hash()[0:bc.difficulty], "0" * bc.difficulty)
        self.assertEqual(bc.chain[-1], block)
        
        block2 = Block(3, 'Some data', block.hash(), 0)
        
        bc.mine(block2)
        
        self.assertEqual(block2.hash()[0:bc.difficulty], "0" * bc.difficulty)
        self.assertEqual(bc.chain[-1], block2)
        
    def test_blockchain_validation(self):
        bc = Blockchain(True)
        block = Block(2, prev_hash=bc.chain[-1].hash())
        
        bc.mine(block)
        
        block2 = Block(3, 'Some data', block.hash(), 0)
        
        bc.mine(block2)
        
        self.assertTrue(bc.is_valid())
        
        bc.chain[1].data = 'different data'
        
        self.assertFalse(bc.is_valid())
        
        bc.mine(bc.chain[1])
        
        self.assertFalse(bc.is_valid())
    
    def test_granting_money(self):
        bc = Blockchain(True)
        
        self.assertEqual(bc.get_user_balance('abc'), 100)


if __name__ == '__main__':
    unittest.main()