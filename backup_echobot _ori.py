





#class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

#    async def on_message_activity(self, turn_context: TurnContext):

 #       await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

  #  async def on_members_added_activity(
    #    self,
   #     members_added: ChannelAccount,
     #   turn_context: TurnContext
   # ):
    #    for member_added in members_added:
     #       if member_added.id != turn_context.activity.recipient.id:
      #          await turn_context.send_activity("Hello and welcome!")







# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import os
import openai
import requests

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        openai.api_type = "azure"
        openai.api_base = "https://bsdsopenai.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "f9475c4a5507403b9148caff0bf86a35"

        response = openai.ChatCompletion.create(
          engine="gpt35TurboTesting",
          messages = [{"role": "user", "content": turn_context.activity.text}], #"{{role}:{system},{content}:{text_in}}", #[{"role":"system","content":"You are an AI assistant that helps people find information."}],
          #prompt="'{ turn_context.activity.text }'", # "# Write a python function to reverse a string. The function should be an optimal solution in terms of time and space complexity.\n# Example input to the function: abcd123\n# Example output to the function: 321dcba",
          temperature=0.7,
          max_tokens=800,
          top_p=0.95,
          frequency_penalty=0,
          presence_penalty=0,
          stop=None)

         # Access the generated text
        generated_text = response.choices[0].message['content'] #response['choices'][0]['text']
        
        await turn_context.send_activity(f"{ generated_text }")



    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to BSDS Testing Bot!")




#class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

#    async def on_message_activity(self, turn_context: TurnContext):

 #       await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

  #  async def on_members_added_activity(
    #    self,
   #     members_added: ChannelAccount,
     #   turn_context: TurnContext
   # ):
    #    for member_added in members_added:
     #       if member_added.id != turn_context.activity.recipient.id:
      #          await turn_context.send_activity("Hello and welcome!")
