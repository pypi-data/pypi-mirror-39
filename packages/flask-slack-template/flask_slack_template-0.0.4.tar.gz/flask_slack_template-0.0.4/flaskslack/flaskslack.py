import json
from threading import Thread

import requests
from flask import abort, request, jsonify, Flask, make_response

from flaskslack.slack import Slack, ResponseType


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def parameterized_decorator_instance(dec):
    """
    Meta-decorator that allows an instance method decorator to have parameters
    """
    def layer(self, *args, **kwargs):
        def repl(f):
            return dec(self, f, *args, **kwargs)
        return repl
    return layer


def delayed_message(func: callable, response_type: ResponseType):
    """
    Sends a POST request to the response_url located in the form_content.
    See: https://api.slack.com/slash-commands#sending_delayed_responses
    :param func: The actual implementation function that does the logic.
            It should return a dict. dict should contain 'text', and/or a list of 'attachments'.
            See: https://api.slack.com/slash-commands#responding_immediate_response
    :param response_type:
    :return:
    """

    def decorator(form_content: dict):

        # if response_url does not exist,
        # then the form_content might be wrapped inside a "payload"
        if "response_url" not in form_content:
            if "payload" not in form_content:
                raise ValueError("response_url or payload not in form_content")
            form_content = json.loads(form_content["payload"])

        response_url = form_content["response_url"]

        try:
            json_response = func(form_content)
        except Exception:
            error_json = {
                'text': "500 Internal Server Error: The server encountered an internal error and was unable to complete your request."
                        " Either the server is overloaded or there is an error in the application.",
                'response_type': ResponseType.EPHEMERAL.value
            }

            requests.post(response_url, json=error_json)
            raise
        else:
            # send a delayed response to response_url
            json_response['response_type'] = response_type.value
            requests.post(response_url, json=json_response)

    return decorator


class FlaskSlack:
    def __init__(self, app: 'Flask', slack: 'Slack' = Slack.create()):
        self.app = app
        self.slack = slack

    @parameterized_decorator_instance
    def slack_route(self, func: callable, route: str, response_type: ResponseType,
                    verify_signature: bool=True, empty_immediate_response: bool=False):
        """
        a decorator method that wraps an implementation method to allow for receiving and responding to slack
        slash commands
        :param func: the function to run
        :param route: the slack endpoint to route traffic from
        :param response_type: If EPHEMERAL, posts will only be to the calling user, if IN_CHANNEL, the slack message
        will be public
        :param verify_signature: should almost always be true. Set this to false if you need to debug locally
        :param empty_immediate_response: If true, returns an empty immediate response no matter what. This is necessary
        to deal with some weirdness while dealing with interactive messages
        """

        @self.app.route(route, methods=['POST'], endpoint=route)  # TODO endpoint hack to fix name conflict
        def decorator():
            # verify that the request is from slack
            if verify_signature:
                try:
                    raw_body = request.get_data()
                    slack_request_timestamp = request.headers['X-Slack-Request-Timestamp']
                    slack_signature = request.headers['X-Slack-Signature']
                    if not self.slack.verify_signature(slack_request_timestamp, slack_signature, raw_body):
                        abort(400, {'message': 'slack verify signature failed'})
                except KeyError:
                    abort(400, {'message': 'slack verification headers missing'})

            # verification passed, handle request in another thread
            form_content = request.form
            delayed_message_func = delayed_message(func, response_type)
            thread = Thread(target=delayed_message_func, args=(form_content,))
            thread.start()

            # immediately return 200 OK to let slack know that the message has been received
            if empty_immediate_response:
                return make_response("", 200)
            else:
                return jsonify({"response_type": response_type.value})
        return decorator
