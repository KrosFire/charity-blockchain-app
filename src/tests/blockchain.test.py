from blockchain.blockchain import Blockchain, Block
import unittest


class testingBlockchain(unittest.TestCase): 
    def test_init(self):
        block = Block()
        chain = [block]

        bc = Blockchain(chain)
        
        self.assertEqual(bc.chain[0], block)
        self.assertEqual(len(bc.chain), 1)
        
        bc2 = Blockchain()
        
        self.assertEqual(len(bc2.chain), 1)
        
        genesisBlock = bc2.chain[0]
        
        self.assertEqual(genesisBlock.hash()[0:bc2.difficulty], "0" * bc2.difficulty)
        self.assertEqual(genesisBlock.prev_hash, "0" * 64)
        self.assertEqual(genesisBlock.data, None)

    def test_adding_block(self):
        block = Block()
        
        bc = Blockchain()
        
        bc.add(block)
        
        self.assertEqual(bc.chain[-1], block)
    
    def test_block_mining(self):
        bc = Blockchain()
        block = Block(2, prev_hash=bc.chain[-1])
        
        bc.mine(block)
        
        self.assertEqual(block.hash()[0:bc.difficulty], "0" * bc.difficulty)
        self.assertEqual(bc.chain[-1], block)
        
        block2 = Block(3, 'Some data', block.hash(), 0)
        
        bc.mine(block2)
        
        self.assertEqual(block2.hash()[0:bc.difficulty], "0" * bc.difficulty)
        self.assertEqual(bc.chain[-1], block2)
        
    def test_blockchain_validation(self):
        bc = Blockchain()
        block = Block(2, prev_hash=bc.chain[-1])
        
        bc.mine(block)
        
        block2 = Block(3, 'Some data', block.hash(), 0)
        
        bc.mine(block2)
        
        self.assertTrue(bc.is_valid())
        
        print(bc)
        
        bc.chain[1].data = 'different data'
        
        self.assertFalse(bc.is_valid())
        
        print(bc)
        
        bc.mine(bc.chain[1])
        
        self.assertFalse(bc.is_valid())
        
        print(bc)
if __name__ == '__main__':
    unittest.main()