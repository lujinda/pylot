import random
import unittest

class TestSeq(unittest.TestCase):

    def setUp(self):
        self.seq=range(10)

    def test_shuffle(self):
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq,range(10))
        self.assertRaises(TypeError,random.shuffle,(1,2,3))

    def test_choice(self):
        element=random.choice(self.seq)
        self.assertTrue(element in self.seq)

    def test_sample(self):
        with self.assertRaises(ValueError):
            random.sample(self.seq,20)
        for element in random.sample(self.seq,5):
            self.assertTrue(element in self.seq)

if __name__=="__main__":
    unittest.main()
