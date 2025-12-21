from grader_analyzer.domain.grader.entities.templates import Question


def score_calculator(template: list[Question], user_responses: list[dict]) -> float:
    if len(user_responses) == 0:
        return 0.0
    user_res = [
        {res.get("question", 0): res.get("response", "Z")} for res in user_responses
    ]
    counter = 0
    for temp_res in template:
        for user in user_res:
            has_question = temp_res.question == list(user.keys())[0]
            has_answer = temp_res.answer == list(user.values())[0]
            if has_question and has_answer:
                counter += 1
    return round(counter / len(template) * 5, 1)
