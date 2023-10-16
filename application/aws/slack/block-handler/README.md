# Slack-Block-Handler
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Slack-Block-Handler?tab=code)

This AWS Lambda function handles block kit interactions from a Slack application. Block kits are a UI framework for Slack applications that can include a range of elements, like interactive buttons, select menus, or date pickers. 

## Functionality

This function performs several checks and actions:

1. Checks if the interaction is from an end user and triggered by a button click within the block kit.
2. It updates the message in Slack to reflect that it's no longer editable, showing the question asked and the chatbot chosen.
3. The processed event is then sent to an SQS queue for further processing.

Here's a more detailed process:

- It verifies if the request is less than 5 minutes old to avoid replay attacks.
- Converts event body from BASE64 and URL parameterized formats if required.
- The payload from the body of the event is parsed.
- It checks for user actions within the payload. If there's no action or the action is not a button click with value 'question_sent', the function ends.
- It fetches and updates values from the payload and forms a new dictionary with relevant values.
- Fetches the account details from Supabase based on the Slack team id.
- Forms a block of message to post back to Slack with a confirmation message about the question being sent and the details of the chatbot and the question.
- Updates the message in the Slack channel with the formed blocks using the Slack chat.update API.
- It then sends a slack_record to the SQS queue for further processing. The slack_record includes the question asked, the chatbot chosen, the channel ID, Slack team ID, the timestamp of the message, and a flag indicating whether it's an original question.

