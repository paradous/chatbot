
from botbuilder.schema import InputHints
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, UserState

from src.nlu import Intent, NLU
from . import BookingRoomDialog
from .utils import Emoji
from .helpers import NLUHelper


class MainDialog(ComponentDialog):

    def __init__(self, nlu_recognizer: NLU, user_state: UserState,
                 booking_room_dialog: BookingRoomDialog):

        super(MainDialog, self).__init__(MainDialog.__name__)

        # Load the NLU module
        self._nlu_recognizer = nlu_recognizer

        # Load the sub-dialogs
        self._booking_dialog_id = booking_room_dialog.id

        # Setup the waterfall dialog
        self.add_dialog(WaterfallDialog(WaterfallDialog.__name__, [
            self.intro_step,
            self.act_step,
            self.final_step
        ]))

        # Append the prompts and custom dialogs, used in the waterfall
        self.add_dialog(TextPrompt("ActPrompt"))
        self.add_dialog(booking_room_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__

    @staticmethod
    async def intro_step(step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Intro step. Triggered upon any interaction from the user to this bot.
        """

        # Ask what to do
        message = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )

        # TextPromp - How can I help you ?
        return await step_context.prompt(
            "ActPrompt",
            PromptOptions(
                prompt=MessageFactory.text(message)
            ),
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Act step. Take user response and infer its intention.
        Dispatch to the desired sub-dialog
        """

        intent, keywords = await NLUHelper.execute_nlu_query(
            self._nlu_recognizer, step_context.result
        )

        # Run the BookingRoomDialog, passing it keywords from nlu
        if intent == Intent.BOOK_ROOM:
            return await step_context.begin_dialog(self._booking_dialog_id, keywords)

        # If no intent was understood, return a didn't understand message
        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )

            await step_context.context.send_activity(
                MessageFactory.text(
                    didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
                )
            )

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Final step. Triggered upon sub-dialog completion. Replace the current
        dialog by the main dialog to start a new loop of conversation.
        """

        # Replace the current dialog back to main dialog
        return await step_context.replace_dialog(
            self.id,
            "What else can I do for you?"
        )
