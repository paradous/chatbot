
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions, Activity, ActivityTypes
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, AttachmentPrompt, PromptOptions, PromptValidatorContext
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from src.nlu import Intent, NLU
from .utils import Emoji
from .helpers import NLUHelper
from .data_models import RoomReservation


class BookingRoomDialog(ComponentDialog):

    def __init__(self, nlu_recognizer: NLU, user_state: UserState):
        super(BookingRoomDialog, self).__init__(BookingRoomDialog.__name__)

        # Load the NLU module
        self._nlu_recognizer = nlu_recognizer

        # Load the RoomReservation class
        self.room_reservation_accessor = user_state.create_property("RoomReservation")

        # Setup the waterfall dialog
        self.add_dialog(WaterfallDialog("WFBookingDialog", [
            self.people_step,
            self.duration_step,
            self.breakfast_step,
            self.summary_step,
        ]))

        # Append the prompts and custom prompts
        self.add_dialog(NumberPrompt("PeoplePrompt", BookingRoomDialog.people_prompt_validator))
        self.add_dialog(NumberPrompt("DurationPrompt", BookingRoomDialog.duration_prompt_validator))
        self.add_dialog(ConfirmPrompt("IsTakingBreakfastPrompt"))

        self.initial_dialog_id = "WFBookingDialog"

    @staticmethod
    async def people_step(step_context: WaterfallStepContext) -> DialogTurnResult:
        """Ask the user: how many people to make the reservation?"""

        # Retrieve the booking keywords
        booking_keywords: dict = step_context.options
        step_context.values['booking_keywords'] = booking_keywords

        # If the keyword 'people' exists and is filled, pass the question
        if 'people' in booking_keywords and booking_keywords['people'] is not None:
            return await step_context.next(booking_keywords['people'])

        # Give user suggestions (1 or 2 people).
        # The user can still write a custom number of people [1, 4].
        options = PromptOptions(
            prompt=Activity(

                type=ActivityTypes.message,
                text="Would you like a single or a double room?",

                suggested_actions=SuggestedActions(
                    actions=[
                        CardAction(
                            title="Single",
                            type=ActionTypes.im_back,
                            value="Single room (1 people)"
                        ),
                        CardAction(
                            title="Double",
                            type=ActionTypes.im_back,
                            value="Double room (2 peoples)"
                        )
                    ]
                )
            ),
            retry_prompt=MessageFactory.text(
                "Reservations can be made for one to four people only."
            )
        )

        # NumberPrompt - How many people ?
        return await step_context.prompt(
            "PeoplePrompt",
            options
        )

    @staticmethod
    async def duration_step(step_context: WaterfallStepContext) -> DialogTurnResult:
        """Ask the user: how many night to reserve?"""

        # Save the number of people
        step_context.values["people"] = step_context.result

        # Retrieve the keywords
        booking_keywords: dict = step_context.values["booking_keywords"]

        # If the keyword 'duration' exists and is filled, pass the question
        if 'duration' in booking_keywords and booking_keywords['duration'] is not None:
            return await step_context.next(booking_keywords['duration'])

        # NumberPrompt - How many nights ? (duration)
        return await step_context.prompt(
            "DurationPrompt",
            PromptOptions(
                prompt=MessageFactory.text("How long do you want to stay?"),
                retry_prompt=MessageFactory.text(
                    "It is only possible to book from 1 to 7 nights"
                ),
            ),
        )

    @staticmethod
    async def breakfast_step(step_context: WaterfallStepContext) -> DialogTurnResult:

        # Save the number of nights
        step_context.values["duration"] = step_context.result

        # Confirm people and duration
        await step_context.context.send_activity(
            MessageFactory.text(
                f"Okay, so {step_context.values['people']} people for {step_context.values['duration']} nights"
            )
        )

        # ConfirmPrompt - Is taking breakfast ?
        return await step_context.prompt(
            "IsTakingBreakfastPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Will you be having breakfast?")
            ),
        )

    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        # Save if the user take the breakfast (bool)
        step_context.values["breakfast"] = step_context.result

        # If the user said "Yes":
        if step_context.result:

            # Confirm breakfast hour
            await step_context.context.send_activity(
                MessageFactory.text(f"Perfect, breakfast is from 6am to 10am")
            )

        # Save information to Reservation object
        room_reservation = await self.room_reservation_accessor.get(
            step_context.context, RoomReservation
        )

        room_reservation.people = step_context.values["people"]
        room_reservation.duration = step_context.values["duration"]
        room_reservation.breakfast = step_context.values["breakfast"]

        # End the dialog
        await step_context.context.send_activity(
            MessageFactory.text("Your booking has been made !")
        )

        return await step_context.end_dialog()

    @staticmethod
    async def people_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """Validate the number of people entered by the user."""

        # Restrict people between [1 and 4].
        return (
                prompt_context.recognized.succeeded
                and 1 <= prompt_context.recognized.value <= 4
        )

    @staticmethod
    async def duration_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """Validate the number of nights entered by the user."""

        # Restrict nights between [1 and 7].
        return (
                prompt_context.recognized.succeeded
                and 1 <= prompt_context.recognized.value <= 7
        )
