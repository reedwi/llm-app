# Monday-Delete-Chatbot
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Monday-Delete-Chatbot?tab=code)

This project is an AWS Lambda function designed to handle chatbot deletion operations when a "Delete Chatbot" button is clicked on a monday.com board. The function interfaces with the Supabase database and monday.com's API to perform its tasks.

## Functionality

When the "Delete Chatbot" button is clicked on the Chatbots board in monday.com, this Lambda function is triggered. It performs the following actions:

1. Retrieves the `itemId` and `boardId` from the event payload.
2. Verifies the JWT token from the request header for security purposes.
3. Fetches the chatbot record from the Supabase database using the `itemId`.
4. If the chatbot record does not exist in Supabase, it logs an error message and updates the item on the Monday board to reflect the error, then terminates.
5. If the chatbot record exists, it deletes the corresponding group and item on the Monday board.
6. Finally, it deletes the chatbot record from the Supabase database.
