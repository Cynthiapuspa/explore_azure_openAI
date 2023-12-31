# Summary_Bot
Simple Discussion and Provide Summary based on User Input using Data from User


Based on sample echo_bot

A bot that echoes back user response.

This bot has been created using [Bot Framework](https://dev.botframework.com), it shows how to create a simple bot that accepts input from the user and echoes it back.

## Prerequisites

This sample **requires** prerequisites in order to run.

### Install Python

## Running Virtual Environment
- Create venv `python -m venv venv`
- Run venv `venv\Scripts\activate.bat`

## Running the sample
- Run `pip install -r requirements.txt` to install all dependencies
- Run `python app.py`

## Convert localhost into public IP
- Install and settings ngrok (https://ngrok.com/docs/getting-started/)
- Run ngrok `ngrok http 3978`
- Copy link https to Azure

### Go to Azure Portal -> Azure Bot -> Configuration -> Messaging endpoint -> `https....ngrok-free.app/api/messages` 

## Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- Enter a Bot URL of `http://localhost:3978/api/messages`
- Enter MicrosoftAppId and MicrosoftAppPassword

### How to use

- Talk to Bot `Say Hello or whathever you want to ask`
- Summary the data please use keyword 'Summary' 
	- Example, `Summary the data : please sum total price for each year and CouncilArea and convert total price into $`
- Summary the data and export to csv, please use keyword 'Summary and csv' 
	- Example, `Summary the data and export to csv : please sum total price for each year and CouncilArea and convert total price into $`

## Enabled Channels (Teams)
In Teams, export to csv still disable. But you can ask the summary or report in chat section.

Enable Teams Channel
### Go to Azure Portal -> Azure Bot -> Channels -> Microsoft Teams -> Enable


## Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Dialogs](https://docs.microsoft.com/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
- [Gathering Input Using Prompts](https://docs.microsoft.com/azure/bot-service/bot-builder-prompts?view=azure-bot-service-4.0&tabs=csharp)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
- [Azure Portal](https://portal.azure.com)
- [Language Understanding using LUIS](https://docs.microsoft.com/azure/cognitive-services/luis/)
- [Channels and Bot Connector Service](https://docs.microsoft.com/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)"# explore_azure_openAI" 
