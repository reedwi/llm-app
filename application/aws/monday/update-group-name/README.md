# Monday-Update-Group-Name
[Lambda Link](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/Monday-Update-Group-Name?tab=code)

This AWS Lambda function is triggered when an item name is changed on the Chatbots board in Monday.com. The function subsequently updates the corresponding group name in the Documents board.

## Functionality

The function executes the following operations in response to a change in item name:

1. Extracts the authorization token, item ID, and board ID from the incoming event.
2. Decodes the token using the signing secret key, which should be provided as an environment variable (`MONDAY_SIGNING_SECRET`).
3. Retrieves the chatbot row from the Supabase database corresponding to the item ID. If there's no matching row, it logs an error and ends the function.
4. Using the short-lived token from the decoded header, it fetches the item details from Monday.com. The item's name is extracted, and if the name is not found, the function returns successfully without updating the group name.
5. Using the same token, it updates the group name on the Documents board in Monday.com to match the item's name.
6. Updates the chatbot row in the Supabase database with the new name.
7. Returns a success message.
