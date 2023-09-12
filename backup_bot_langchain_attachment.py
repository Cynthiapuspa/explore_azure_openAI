# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)
import os
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
import openai
from langchain.agents.agent_types import AgentType
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
import pyodbc
import pandas.io.sql as sql

class MyBot(ActivityHandler):
    
    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        if (turn_context.activity.attachments and len(turn_context.activity.attachments) > 0):
            await self._handle_outgoing_attachment(turn_context)
        else:
            await self._handle_outgoing_attachment(turn_context)
        
        await self._display_options(turn_context)
            

    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added :
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to BSDS Bot {member.name}!")
                await self._display_options(turn_context)


    async def _display_options(self, turn_context: TurnContext):
        """
        Create a HeroCard with options for the user to interact with the bot.
        :param turn_context:
        :return:
        """

        # Note that some channels require different values to be used in order to get buttons to display text.
        # In this code the emulator is accounted for with the 'title' parameter, but in other channels you may
        # need to provide a value for other parameters like 'text' or 'displayText'.
        card = HeroCard(
            text="You can asking about summary in chat section or export into file, please select one of the following choices",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back, title="1. Summary the data in chat section", value="1"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="2. Summary the data and export into csv file", value="2"
                ),
                CardAction(
                    type=ActionTypes.im_back, title="3. Summary the data and export into excel file", value="3"
                ),
            ],
        )

        reply = MessageFactory.attachment(CardFactory.hero_card(card))
        await turn_context.send_activity(reply)


    async def _handle_outgoing_attachment(self, turn_context: TurnContext):
        reply = Activity(type=ActivityTypes.message)

        first_char = turn_context.activity.text[0]
        if first_char == "1":
            reply.text = "This is an chat section."
            turn_context.activity.text = "Hello"
            await self._chat_activity(turn_context)
        else:
            reply.text = "Your input was not recognized, please try again."

            await turn_context.send_activity(reply)

    async def _chat_section_bot(self, input_user: TurnContext):

        openai.api_type = "azure"
        openai.api_base = "https://bsdsopenai.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "f9475c4a5507403b9148caff0bf86a35"

        response = openai.ChatCompletion.create(
            engine="gpt35TurboTesting",
            messages = [{"role": "user", "content": input_user}], #"{{role}:{system},{content}:{text_in}}", #[{"role":"system","content":"You are an AI assistant that helps people find information."}],
            #prompt="'{ turn_context.activity.text }'", # "# Write a python function to reverse a string. The function should be an optimal solution in terms of time and space complexity.\n# Example input to the function: abcd123\n# Example output to the function: 321dcba",
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None)
        
        #Access the generated text
        generated_text = generated_text(response.choices[0].message['content']) #response['choices'][0]['text']
        
        await turn_context.send_activity(f"{ generated_text }")
        #await turn_context.send_activity(f"{ generated_text }")
    
    async def _chat_activity(self, turn_context: TurnContext):

        async def _chat_section_activity(
            self,
            members_added: ChannelAccount,
            turn_context: TurnContext
        ):
            for member_added in members_added:
                if member_added.id != turn_context.activity.recipient.id:
                    await turn_context.send_activity("Welcome to BSDS Chat Room Bot {member.name}!")


        async def _chat_section_summary(self, turn_context: TurnContext): 
    
            input_user = turn_context.activity.text 

            if input_user.lower().find('summary') < 0:
                generated_text = [self._chat_section_bot(input_user)]
            
            elif input_user.lower().find('summary') >= 0:
                # Configure Azure OpenAI
                OPENAI_API_TYPE = "azure"
                OPENAI_API_BASE = "https://bsdsopenai.openai.azure.com/"
                OPENAI_API_VERSION = "2023-07-01-preview"
                OPENAI_API_KEY = "f9475c4a5507403b9148caff0bf86a35"

                os.environ["OPENAI_API_TYPE"] = OPENAI_API_TYPE
                os.environ["OPENAI_API_VERSION"] = OPENAI_API_VERSION
                os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
                os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

                #df = pd.read_csv(r"C:\Users\Cynthia.Anggraeni\echo_bot\Melbourne_housing_FULL.csv"

                conn = pyodbc.connect("DSN=MyAzureDatabricks_DSN", autocommit=True)

                # run a SQL query using the connection you created
                cursor = conn.cursor()
                query = "SELECT * FROM default.melbourne_housing limit 100"

                pd.set_option('display.max_columns', None)
                df = pd.read_sql_query(query, conn)

                df['Date'] = pd.to_datetime(df['Date'], format = "%d/%m/%Y")
                df['Price'] = df['Price'].fillna(0)
                df['Bedroom2'] = df['Bedroom2'].fillna(0)
                df['Bathroom'] = df['Bathroom'].fillna(0)
                df['Car'] = df['Car'].fillna(0)
                df['Landsize'] = df['Landsize'].fillna(0)
                df['BuildingArea'] = df['BuildingArea'].fillna(0)
                df['YearBuilt'] = df['YearBuilt'].fillna(0)
                df['Lattitude'] = df['Lattitude'].fillna(0)
                df['Longtitude'] = df['Longtitude'].fillna(0)


                # Create an AzureOpenAI instance
                llm = AzureOpenAI(
                    # openai_api_type="azure",
                    deployment_name="test-demo", 
                    model_name="gpt-35-turbo",
                    callbacks=[FinalStreamingStdOutCallbackHandler()]
                    ) 
            
                agent = create_pandas_dataframe_agent(
                        llm,
                        df,
                        verbose=True,
                )

                generated_text = agent.run(input_user)
            
                # Close the connection when done
                conn.close()

            await turn_context.send_activity(f"{ generated_text }")