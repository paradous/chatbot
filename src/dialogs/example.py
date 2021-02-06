
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, AttachmentPrompt, PromptOptions, PromptValidatorContext
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from .data_models import UserProfile


class UserProfileDialog(ComponentDialog):

    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)

        # Load the UserProfile class
        self.user_profile_accessor = user_state.create_property("UserProfile")

        # Setup the waterfall dialog
        self.add_dialog(WaterfallDialog(WaterfallDialog.__name__, [
            self.people_step,
            self.nights_step,
            self.breakfast_step,
            self.summary_step,
        ]))

        # Append the prompts and custom prompts
        # self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    @staticmethod
    async def people_step(step_context: WaterfallStepContext) -> DialogTurnResult:

        # ChoicePrompt - How many people ?
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("What size room will you need?"),
                choices=[
                    Choice("2 peoples"),
                    Choice("4 peoples"),
                ],
            ),
        )

    @staticmethod
    async def nights_step(step_context: WaterfallStepContext) -> DialogTurnResult:

        # Save the number of people
        step_context.values["peoples"] = step_context.result.value

        # Confirm the number of people
        await step_context.context.send_activity(
            MessageFactory.text(f"Okay, for {step_context.result.value}")
        )

        # NumberPrompt - How many nights ?
        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("How long do you want to stay?")
            ),
        )

    @staticmethod
    async def breakfast_step(step_context: WaterfallStepContext) -> DialogTurnResult:

        # Save the number of nights
        step_context.values["nights"] = step_context.result

        # ConfirmPrompt - Is taking breakfast ?
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Will you be having breakfast?")
            ),
        )

    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        # If the user said True:
        if step_context.result:

            # Confirm breakfast hour
            await step_context.context.send_activity(
                MessageFactory.text(f"Perfect, breakfast is from 6am to 10am.")
            )

        # Save information to Reservation object
        user_profile = await self.user_profile_accessor.get(
            step_context.context, UserProfile
        )

        """
        user_profile.transport = step_context.values["transport"]
        user_profile.name = step_context.values["name"]
        user_profile.age = step_context.values["age"]
        user_profile.picture = step_context.values["picture"]
        """

        # End the dialog
        await step_context.context.send_activity(
            MessageFactory.text("Thanks. See you !")
        )

        return await step_context.end_dialog()
