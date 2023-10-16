# Slack-Queue-Poller
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Slack-Queue-Poller?tab=code)


**TODO**

Did not know about lambda layers at the time. Will eventually want to refactor so that this can be used by a layer instead of building an entire package


The `Slack-Queue-Poller` is an AWS Lambda function designed to process messages sent to an Amazon SQS (Simple Queue Service) queue. It retrieves a user's question and decides which chatbot to use for interaction. The function also fetches the thread history, if available, and uses the Langchain module to get an answer to the question from a Pinecone index, along with the sources.

## Description

The main goal of this function is to enable effective interaction between users and chatbots, where the chatbot is able to answer questions and provide sources for its answers.

## Functionality

1. **Message Retrieval**: The function pulls messages from the specified SQS queue.
2. **Message Processing**: Each message contains data such as the Slack team ID, the chatbot namespace, the timestamp of the message, the question, and the Slack channel ID. All these are extracted and used in subsequent steps.
3. **Message Deletion**: Once the message has been processed, it's deleted from the SQS queue to avoid processing it again in the future.
4. **Chatbot Selection**: The function queries the 'accounts' table in a Supabase database to fetch the account linked to the Slack team ID.
5. **Chat History Retrieval**: If there is an original question in the message, it implies a follow-up question, in which case the chat history isn't fetched. If not, it fetches the chat history associated with the message.
6. **Answer Retrieval**: It uses the Langchain module to fetch an answer to the question from a Pinecone index. 
7. **Posting Answer**: The function posts the answer in the relevant Slack thread. If the answer doesn't come from ChatGPT, the source documents are processed and appended to the answer.
8. **Usage Logging**: Finally, the function logs the usage data in the 'usage' table in Supabase for accounting purposes.
