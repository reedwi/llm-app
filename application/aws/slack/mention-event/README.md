# Slack-Mention-Event
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Slack-Mention-Event?tab=code)

This AWS Lambda function is designed to handle mention events from a Slack application. The function is triggered when the Slack bot is mentioned. It makes sure that it's only triggered by end user messages, not by bot messages or hidden messages. If a thread timestamp is not in the event, it posts a default message in response. If a thread timestamp is present, the function fetches the thread history and formats an event which is then sent to an SQS queue for further processing.

## Functionality

Here's a detailed look at the lambda function's process:

1. Filters out bot messages, hidden messages, or messages with a bot id to prevent the bot from triggering itself.
2. If the event doesn't have a 'thread_ts' (indicating it's not part of a thread), it selects the relevant account from the Supabase 'accounts' table by matching the 'slack_team_id' with the team id from the event body. Then, the function posts a message to the Slack channel suggesting to use the '/askobo' slash command to initiate a question.
3. If the event has a 'thread_ts', the function fetches the account details just like in step 2, and then uses Slack's conversations.replies API to get the thread history.
4. From the thread history, it determines the name of the chatbot that was originally asked the question, which it uses to determine the chatbot's internal name. 
5. The function then constructs a slack_record dictionary which includes the new question text, chatbot name, channel ID, Slack team ID, and the timestamp of the message.
6. This record is then sent as a message to the specified SQS queue for further processing.
