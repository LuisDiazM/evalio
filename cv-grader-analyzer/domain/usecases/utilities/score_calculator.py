from typing import List
from domain.entities.templates import Question


def score_calculator(template: List[Question], user_responses: List[dict]) -> float:
    if len(user_responses) == 0:
        return 0.0
    user_res = [{res.get("question", 0): res.get("response", "Z")}
                for res in user_responses]
    counter = 0
    for temp_res in template:
        for user in user_res:
            if temp_res.question == list(user.keys())[0]:
                if temp_res.answer == list(user.values())[0]:
                    counter += 1
    return round(counter / len(template) * 5, 1)
