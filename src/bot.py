
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from src.matching import Matcher
from src.preprocessing import Preprocessor, Tokenizer
from src.classifying import Classifier

# Preprocessing
preprocessor = Preprocessor()
tokenizer = Tokenizer()

# Classifier
classifier = Classifier()
matcher = Matcher()


class Bot(ActivityHandler):

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):

        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):

        # Get the message
        message = turn_context.activity.text

        # Clean the message and create a dataset of tokens
        preprocessed_text = preprocessor.preprocess(message)
        dataset = tokenizer.get_dataset(preprocessed_text)

        # Get the intention
        intent = classifier.predict(dataset)
        keywords = matcher.get_keywords(preprocessed_text, intent)

        return await turn_context.send_activity(
            MessageFactory.text(f"""
            intent: {intent},
            keywords: {keywords}
            """)
        )
