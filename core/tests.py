from django.test import TestCase
from unittest.mock import patch
from .constants import PYTHON_QUESTION_LIST
from .reply_factory import get_next_question, record_current_answer, generate_final_response


class QuizBotTestCase(TestCase):
    def setUp(self):
        self.questions = PYTHON_QUESTION_LIST
        self.expected_answers = {question["question_text"]: question["answer"] for question in self.questions}

    @patch('quiz_bot.get_next_question')
    @patch('quiz_bot.record_current_answer')
    @patch('quiz_bot.generate_final_response')
    def test_quiz_bot_flow(self, mock_generate_final_response, mock_record_current_answer, mock_get_next_question):
        for question in self.questions:
            mock_get_next_question.return_value = question["question_text"]
            mock_record_current_answer.return_value = self.expected_answers.get(question["question_text"], "Sample answer")
            
            answer = mock_get_next_question()
            response = mock_record_current_answer(question["question_text"], answer)

            self.assertEqual(response, self.expected_answers.get(question["question_text"], "Sample answer"))
        
        mock_generate_final_response.return_value = "You scored 90%"

        final_response = mock_generate_final_response()
        self.assertEqual(final_response, "You scored 90%")
        
        self.assertIn("scored", final_response)
        
        for question in self.questions:
            self.assertIn(question["question_text"], mock_get_next_question.call_args_list)

if __name__ == "__main__":
    import unittest
    unittest.main()
