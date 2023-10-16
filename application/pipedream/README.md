# Slack App

Slack App Install
- Do OAuth exchange
- Eventually will update row in accounts supabase table

Slack App Clear Message History
- This may end up getting deleted, but for now it clears all the messages written by the bot in the DM with the end user

# Monday App
Monday App Install
- OAuth flow for Monday app
- Will eventually be an update for the accounts table with the install flow once finalized

Delete Namespace from Index
- When someone deletes a chatbot through the Monday board it goes to a lambda function and I send to here to actually remove the chatbot from the pinecone index because it was easy to complete in pipedream

# Payments and Subscriptions
Payments
- In progress, but will be responsible for creating an account initially

Subscriptions
- In progress, but will be responsible for keeping track of subscription status for people