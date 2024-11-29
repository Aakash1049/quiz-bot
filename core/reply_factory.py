
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer:
        return False, "Answer cannot be empty."
    if not current_question_id:
        return False, "Invalid question identifier."

    if 'answers' not in session:
        session['answers'] = {}  

    session['answers'][current_question_id] = answer
    session.modified = True 

    return True, "Answer recorded successfully."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if not isinstance(current_question_id, int) or current_question_id < 0:
        return None, -1  

    if current_question_id + 1 < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[current_question_id + 1]
        return next_question, current_question_id + 1
    else:
        return None, -1 


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers = session.get('answers', {})
    if not user_answers:
        return "No answers submitted. Your score is 0."

    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_id, question in enumerate(PYTHON_QUESTION_LIST):
        correct_answer = question['answer']
        user_answer = user_answers.get(question_id)
        if user_answer == correct_answer:
            score += 1

    percentage = (score / total_questions) * 100
    result_message = (
        f"Your final score is {score}/{total_questions}.\n"
        f"You got {percentage:.2f}% correct answers.\n"
    )

    if percentage == 100:
        result_message += "Excellent! You aced the quiz!"
    elif percentage >= 75:
        result_message += "Great job! You have a solid understanding."
    elif percentage >= 50:
        result_message += "Good effort! A little more practice will help."
    else:
        result_message += "Keep practicing and you'll improve!"

    return result_message

