# Monday-Training-Queue-Poller
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Monday-Training-Queue-Poller?tab=code)

This is an AWS Lambda function triggered by an Amazon SQS queue, which receives messages from the "Monday-Train-Chatbot" Lambda function. The purpose of this function is to download documents from monday.com and store them into the Supabase object store.

## Functionality

The function executes the following operations in response to an SQS message:

1. Checks the order of the messages in the SQS queue. If there's a message with the `last_asset` flag set to `True` that isn't the last message in the queue, it reorders the messages to make it the last one.
2. Deletes the processed SQS message from the queue to avoid processing it again in the future.
3. Checks if there's an existing bucket in Supabase with the account ID from the message. If not, it creates one.
4. Downloads the document associated with the SQS message from monday.com, stores it locally, and then uploads it to the corresponding bucket in Supabase.
5. After uploading, the function deletes the local copy of the file and creates a new document row in the `documents` table in Supabase, containing information about the document and its location in the bucket.
6. If the document is the last asset for the associated chatbot (i.e., `last_asset` is set to `True`), it inserts a new row into the `chatbot_trainings` table in Supabase, signifying that the chatbot is ready for training.

Note: The `TrainingDocQueueMsg` is a Python data class that models the document data received in the SQS message. It makes it easier to work with the document data by allowing attribute-style access (e.g., `training_doc.asset_id`).
