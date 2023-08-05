from clustaar.schemas.v1 import WEBHOOK_REQUEST
from clustaar.schemas.models import Interlocutor, ConversationSession, Coordinates, Step,\
    PauseBotAction, StepReached, WebhookRequest, CustomEvent
import pytest


@pytest.fixture
def action():
    return PauseBotAction()


@pytest.fixture
def step(action):
    return Step(actions=[action],
                name="A step",
                user_data="{}",
                id="1234")


@pytest.fixture
def interlocutor():
    location = Coordinates(lat=1.0, long=2.4)
    return Interlocutor(id="123",
                        email="tintin@moulinsart.fr",
                        first_name="tintin",
                        last_name=None,
                        custom_attributes={"age": "21"},
                        location=location)


@pytest.fixture
def session():
    return ConversationSession(values={"name": "tintin"})


@pytest.fixture
def request(step, session, interlocutor):
    event = StepReached(step=step,
                        session=session,
                        interlocutor=interlocutor,
                        input=CustomEvent(name="event1"),
                        channel="facebook")
    return WebhookRequest(event=event,
                          bot_id="4321",
                          timestamp=1514998709,
                          topic="conversation.step_reached")


@pytest.fixture
def data():
    return {
        "botID": "4321",
        "timestamp": 1514998709,
        "topic": "conversation.step_reached",
        "type": "notification_event",
        "data": {
            "type": "step_reached_event",
            "channel": "facebook",
            "interlocutor": {
                "customAttributes": {"age": "21"},
                "email": "tintin@moulinsart.fr",
                "firstName": "tintin",
                "id": "123",
                "lastName": None,
                "location": {"lat": 1.0, "long": 2.4}
            },
            "session": {
                "values": {"name": "tintin"}
            },
            "step": {
                "actions": [
                    {
                        "type": "pause_bot_action"
                    }
                ],
                "id": "1234",
                "name": "A step",
                "userData": "{}"
            },
            "input": {
                "type": "custom_event",
                "name": "event1"
            }
        }
    }


class TestDump(object):
    def test_returns_a_dict(self, request, mapper, data):
        result = WEBHOOK_REQUEST.dump(request, mapper)
        assert result == data


class TestLoad(object):
    def test_returns_a_request(self, request, mapper, data):
        request = mapper.load(data, WEBHOOK_REQUEST)
        assert isinstance(request, WebhookRequest)
        assert isinstance(request.event, StepReached)
        assert request.event.step.id == "1234"
