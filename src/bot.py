
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from .nlu import NLU
nlu = NLU()


class Bot(ActivityHandler):

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):

        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):

        # Get the intention
        intent, keywords = nlu.get_intent(turn_context.activity.text)

        return await turn_context.send_activity(
            MessageFactory.text(f"""
            intent: {intent},
            keywords: {keywords}
            """)
        )
