
from botbuilder.schema import ChannelAccount
from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState
from botbuilder.dialogs import Dialog

from .dialogs.utils import Emoji
from .dialogs.helpers import DialogHelper


class Bot(ActivityHandler):

    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: Dialog):

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):

        # Send an "Hello" to any new user connected to the bot
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(f"Hello {Emoji.WAVING_HAND.value}")

    async def on_turn(self, turn_context: TurnContext):

        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):

        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
