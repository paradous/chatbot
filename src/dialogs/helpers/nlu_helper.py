
from src.nlu import Intent, NLU


class NLUHelper:

    @staticmethod
    async def execute_nlu_query(nlu_recognizer: NLU, message: str) -> (Intent, dict):

        return nlu_recognizer.get_intent(message)
