# Slack-Development-Slash-Command
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Slack-Development-Slash-Command?tab=code)

The `Slack-Development-Slash-Command` is a Python-based AWS Lambda function that is triggered when the `/askobo` slash command is entered in the Slack application. It responds by generating a block kit that allows the end-user to interact with the chatbots they have access to. Users can select a chatbot, write a question, and send the question for it to be answered.

## Functionality
1. **Authenticity Verification**: The function authenticates the incoming request from Slack to prevent replay attacks and verify the request's origin.
2. **Parameter Parsing**: It then parses the body of the incoming event, converting URL encoded parameters into a Python dictionary.
3. **Chatbot Selection**: The function queries the 'accounts' table in a Supabase database to fetch the account details linked to the 'team_id' parameter from the event body.
4. **Generating Response**: The function queries the 'chatbots' table in the Supabase database to fetch all chatbots linked to the account. It generates a dynamic options list of chatbots and constructs a block kit response that includes a dropdown list to select a chatbot, a text input to type in a question, and a button to submit the question.
5. **Post Message**: Finally, it posts the constructed response block to the appropriate Slack channel using the `chat.postMessage` API endpoint.