from blockchain.data import Data
import rsa
import unittest


class testingBlockchain(unittest.TestCase):
    def gen_key(self):        
        return rsa.newkeys(512, poolsize=2)
    
    def test_hash_validation(self):
        pub_key, priv_key = self.gen_key()
        
        data = Data(priv_key, 'John', 'Mary', 1000)
        
        self.assertEqual(data.verify(pub_key), True)
        self.assertEqual(data.verify('asdad'), False)


if __name__ == '__main__':
    unittest.main()