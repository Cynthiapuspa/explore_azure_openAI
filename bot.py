# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import ActivityHandler, TurnContext
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
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.agents.agent_types import AgentType
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.agents import create_pandas_dataframe_agent
import base64
import os
import openai
import pandas as pd
import pyodbc
import pandas.io.sql as sql

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        
        input_user = turn_context.activity.text 

        if input_user.lower().find('summary') < 0:
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

             # Access the generated text
            generated_text = response.choices[0].message['content'] #response['choices'][0]['text']
        
        elif input_user.lower().find('summary') >= 0:
            text = "/summary"
            date = str(pd.to_datetime('now').date())
            time = str(pd.to_datetime('now').time()).replace(":","_")
            file_name = text + "_" + date + "_" + time[:8] + ".csv"
            path = "C:/Users/Cynthia.Anggraeni/echo_bot/export_file" + file_name

            if input_user.lower().find('csv') >= 0:
                input_user_final = input_user + " into " + path 

            elif input_user.lower().find('csv') < 0:
                input_user_final = input_user

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
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
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

            generated_text = agent.run(input_user_final)
            
            # Close the connection when done
            conn.close()

            if input_user.lower().find('csv') >= 0:
                await self._handle_outgoing_attachment(turn_context, path, file_name)

        await turn_context.send_activity(f"{ generated_text }")


    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to BSDS Testing Bot using langchain!")


    async def _handle_outgoing_attachment(self, turn_context: TurnContext, path, file_name):
        reply = Activity(type=ActivityTypes.message)

        # first_char = turn_context.activity.text[0]
        if turn_context.activity.text.lower().find('csv') >= 0:
            reply.text = "This is an inline attachment."
            reply.attachments = [self._get_inline_attachment(path, file_name)]
        
        await turn_context.send_activity(reply)


    def _get_inline_attachment(self, path, file_name) -> Attachment:
        """
        Creates an inline attachment sent from the bot to the user using a base64 string.
        Using a base64 string to send an attachment will not work on all channels.
        Additionally, some channels will only allow certain file types to be sent this way.
        For example a .png file may work but a .pdf file may not on some channels.
        Please consult the channel documentation for specifics.
        :return: Attachment
        """

        file_path = os.path.join(os.getcwd(), path)
        with open(file_path, "rb") as in_file:
            base64_content = base64.b64encode(in_file.read()).decode()

        return Attachment(
            name=file_name,
            content_type="csv",
            content_url=f"{path}",
        )

        