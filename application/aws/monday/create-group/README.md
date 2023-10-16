# Monday-Create-Group
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Monday-Create-Group?tab=code)

This is an AWS Lambda function that responds to the creation of an item in the Chatbots board on monday.com. The function will create a corresponding group in the Documents board on monday.com, unless the item name matches an already existing item or if there are issues getting the account info from Supabase. The function will also create a corresponding row in the chatbots table in the Supabase database.

## Functionality

The function is triggered when an item is created in the Chatbots board on monday.com. Here's what the function does:

1. Decodes the received JWT token to retrieve the account ID.
2. Checks if the account exists in the Supabase database and retrieves the corresponding account token.
3. Fetches the current chatbots from the database and gets the item from monday.com based on the item ID.
4. Checks if the item name is already used by any other chatbot or if it exists as a group in the Documents board. If so, the function deletes the item and ends the process.
5. If the item name is unique, the function creates a new group in the Documents board using the item name and adds a corresponding row to the chatbots table in the Supabase database.