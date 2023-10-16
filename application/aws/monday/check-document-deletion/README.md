# Monday-Check-Document-Deletion

[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Monday-Check-Document-Deletion?tab=code)

This is an AWS Lambda function that checks for document deletion in monday.com since the last time a chatbot was trained. If a document is found to be deleted, the function updates the status of that document in the database to "DELETE", so the process updating the Pinecone index knows to remove that document.

## Functionality

The function is triggered by the "Monday-Train-Chatbot" event. It carries out the following steps:

1. Parses the event body to obtain `asset_ids` and `chatbot_id`.
2. Fetches the documents associated with the `chatbot_id` from the Supabase database.
3. Determines the documents that were present in the database but are not present in the current `asset_ids` list - these are the documents that have been deleted.
4. For each document identified as deleted, it updates its status in the database to "DELETE".
