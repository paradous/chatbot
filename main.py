
import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from src import Bot
from config import Config

# Load the config and create the bot
config = Config()
bot = Bot()

# Init a Bot adapter https://aka.ms/about-bot-adapter
settings = BotFrameworkAdapterSettings(config.APP_ID, config.APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)


# Catch-all for errors
async def on_error(context: TurnContext, error_: Exception):
    """
    Catch-all functions to write out errors on console log.
    NOTE: In production environment, logging should be done
    to Azure application insights.
    """

    # Print the error into the logs
    print(f"\n [on_turn_error] unhandled error: {error_}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")

    # If the bot is run from the Bot Framework Emulator (dev environment),
    # print a more complete error log.
    if context.activity.channel_id == "emulator":

        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error_}",
            value_type="https://www.botframework.com/schemas/error",
        )
        await context.send_activity(trace_activity)

adapter.on_turn_error = on_error


# Direct message API
async def messages(req: Request) -> Response:
    """
    Main bot function: Listen for incoming API request.
    Route: '/api/messages'.
    """

    # Filter only JSON requests
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    # Deserialize the JSON
    activity = Activity().deserialize(body)

    # Retrieve the authorization code if sent
    auth_header = ""
    if "Authorization" in req.headers:
        auth_header = req.headers["Authorization"]

    # Call the bot and send back its response
    response = await adapter.process_activity(activity, auth_header, bot.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)

    # Return HTTP-200 if no response is send back
    return Response(status=HTTPStatus.OK)

# Init and open routes for direct API call
app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_post("/api/messages", messages)


if __name__ == "__main__":

    web.run_app(app, host="0.0.0.0", port=config.PORT)

    """
    from src.matching import Matcher
    matcher = Matcher()
    result = matcher.get_keywords("I wish to reserve a room for 2 peoples", "longtalk_hotel_reserve")
    print(result)
    """
