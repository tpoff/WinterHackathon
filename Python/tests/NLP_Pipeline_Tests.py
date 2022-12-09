import unittest
from NLP_Pipeline.NLP_Pipeline import NLP_Pipeline



class MyTestCase(unittest.TestCase):
    def test_base_subject_extraction(self):
        pipeline = NLP_Pipeline()
        predicted_subject, _ = pipeline.nlp_get_subject("Tell me about Dallas Texas")

        self.assertEqual(predicted_subject, "Dallas Texas")



if __name__ == '__main__':
    unittest.main()
