import unittest
from NLP_Pipeline.NLP_Pipeline import NLP_Pipeline



class MyTestCase(unittest.TestCase):
    def test_base_subject_extraction(self):
        pipeline = NLP_Pipeline()
        predicted_subject, _ = pipeline.nlp_get_subject("Tell me about Dallas Texas")

        self.assertEqual(predicted_subject, "Dallas Texas")

    def test_major_subject_extraction(self):
        sentences = [
            ("show me pics of downtown Dallas.", "images"),
            ("show me Dallas videos.", "videos"),
            ("tell me about Dallas.", "info"),
            ("general info about Dallas.", "info"),
            ("what is Dallas.", "info"),
            ("what is the history of Dallas.", "info"),
            ("when was Dallas Founded.", "info"),
            ("tell me about Dallas's past.", "info"),
            ("When was the last slave Freed in Texas?", "info"),
            ("Things to do in Dallas", "info"),
            ("site seeing Dallas", "info"),
            ("Places to go Dallas", "info"),
            ("Places to eat Dallas", "info"),
            ("Dallas nightlife", "info"),
            ("5 start hotels Dallas", "info"),
            ("Dallas housing", "info"),
        ]
        pipeline = NLP_Pipeline()
        for sentence, major_class in sentences:
            predicted_class, _ = pipeline.nlp_get_major_category(sentence)
            self.assertEqual(predicted_class, major_class)

    def test_info_sub_subject_extraction(self):
        sentences = [
            ("tell me about Dallas.", "general"),
            ("general info about Dallas.", "general"),
            ("what is Dallas.", "general"),
            ("what is the history of Dallas.", "history"),
            ("when was Dallas Founded.", "history"),
            ("tell me about Dallas's past.", "history"),
            ("When was the last slave Freed in Texas?", "history"),
            ("Things to do in Dallas", "tourist"),
            ("site seeing Dallas", "tourist"),
            ("Places to go Dallas", "tourist"),
            ("Places to eat Dallas", "tourist"),
            ("Dallas nightlife", "tourist"),
            ("5 start hotels Dallas", "tourist"),
            ("Dallas housing", "tourist"),
        ]
        pipeline = NLP_Pipeline()
        for sentence, major_class in sentences:
            predicted_class, _ = pipeline.nlp_get_info_category_strat_multi_point_category(sentence)
            self.assertEqual(predicted_class, major_class)
    def test_pipeline_subject_intent_extraction(self):
        sentences = [
            ("tell me about Dallas.", "general", "Dallas"),
            ("general info about Dallas.", "general", "Dallas"),
            ("what is Dallas.", "general", "Dallas"),
            ("what is the history of Dallas.", "history", "Dallas"),
            ("when was Dallas founded.", "history", "Dallas"),
            ("tell me about Dallas past.", "history", "Dallas"),
            ("When was the last slave Freed in Texas?", "history", "Texas"),
            ("Things to do in Dallas", "tourist", "Dallas"),
            ("site seeing Dallas", "tourist", "Dallas"),
            ("Places to go Dallas", "tourist", "Dallas"),
            ("Places to eat Dallas", "tourist", "Dallas"),
            ("Dallas nightlife", "tourist", "Dallas"),
            ("5 start hotels Dallas", "tourist", "Dallas"),
            ("Dallas housing", "tourist", "Dallas"),
        ]
        pipeline = NLP_Pipeline()
        for sentence, major_class, subject in sentences:
            predicted_subject, predicted_class = pipeline.pipeline(sentence)
            self.assertEqual(predicted_class, major_class)
            self.assertEqual(predicted_subject, subject)
    def test_pipeline_subject_intent_extraction_lowercase(self):
        sentences = [
            ("tell me about Dallas.", "general", "Dallas"),
            ("general info about Dallas.", "general", "Dallas"),
            ("what is Dallas.", "general", "Dallas"),
            ("what is the history of Dallas.", "history", "Dallas"),
            ("when was Dallas founded.", "history", "Dallas"),
            ("tell me about Dallas past.", "history", "Dallas"),
            ("When was the last slave Freed in Texas?", "history", "Texas"),
            ("Things to do in Dallas", "tourist", "Dallas"),
            ("site seeing Dallas", "tourist", "Dallas"),
            ("Places to go Dallas", "tourist", "Dallas"),
            ("Places to eat Dallas", "tourist", "Dallas"),
            ("Dallas nightlife", "tourist", "Dallas"),
            ("5 start hotels Dallas", "tourist", "Dallas"),
            ("Dallas housing", "tourist", "Dallas"),
        ]
        pipeline = NLP_Pipeline()
        for sentence, major_class, subject in sentences:
            sentence = sentence.lower()
            subject = subject.lower()
            predicted_subject, predicted_class = pipeline.pipeline(sentence)
            self.assertEqual(predicted_class, major_class)
            self.assertEqual(predicted_subject, subject)



if __name__ == '__main__':
    unittest.main()
