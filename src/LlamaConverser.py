import json
from llamaapi import LlamaAPI

class LlamaConv():
    def __init__(self):
        self.llama = LlamaAPI("LL-d2MzDgTl9wpcCX1gTxXgyTNrvJi6EVY4Gp7dU5M8hcroeECyHlzLKVEtLdsci7j8")

    def converse(self, message):
        # Build the API request
        api_request_json = {
            "messages": [
                {"role": "system", "content": "Your answer must be lesss 200 caracters."},
                {"role": "user", "content": message},
            ]
        }

        # Execute the Request
        response = self.llama.run(api_request_json)

        return response.json()["choices"][0]["message"]["content"]
