# Monday-Train-Chatbot
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Monday-Train-Chatbot?tab=code)

This is an AWS Lambda function that responds to a "Train Chatbot" button click event on the Chatbots board in monday.com. The primary purpose of the function is to identify all the items in the Documents board that require processing and to add them into the Pinecone index for the specific chatbot.

## Functionality

The function is triggered when the "Train Chatbot" button is clicked on the Chatbots board on monday.com. Here's what the function does:

1. Decodes the received JWT token to retrieve the account ID and validates the status of the chatbot model.
2. Fetches the account and account access from the Supabase database.
3. Fetches the chatbot row from the Supabase database corresponding to the clicked item ID.
4. If the chatbot's model is already building, the function terminates the process to avoid overlapping processes.
5. If the chatbot's model is not building, the function updates the status of the chatbot to "Model is Building" on the Chatbots board.
6. Fetches all item IDs from the Documents board associated with the chatbot.
7. If no item IDs are found or an error occurs, the function updates the status of the chatbot to "ERROR" on the Chatbots board and terminates the process.
8. If item IDs are found, the function fetches the values and assets for each item.
9. Filters out items that do not belong to the current chatbot group or whose status is not "Updated". The function also updates the status of documents with no assets to "New" on the Documents board.
10. For each asset in the filtered items, the function parses document information and determines whether the asset is the last asset of the item.
11. The parsed documents are then sent to another Lambda function for further processing, and each document is also sent to an SQS queue for subsequent processing.
12. The function also sends asset IDs and the chatbot ID to another Lambda function to determine any asset deletions needed.

Note: The actual document processing and addition to the Pinecone index are performed outside this function
