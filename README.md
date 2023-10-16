# Monday Slack ChatGPT App
Project to create custom LLMs for businesses based on internal documentation.
- Documents stored and organized in Monday via a Monday App
- Project level information stored in supabase database and indexes stored in Pinecone
- Front-end UI and interaction with custom LLM surfaced through a Slack App
- Pipedream and Lambda handling serving and retrieving end user requests from slack
- Lambda handling requests from Monday app

## Slack App
- [x] Create Slack App
- [x] Have frontend component of slack app in working space
- [x] Backend functionality of slack app
- [x] Langchain in a working state for QA with bot in slack
- [x] Fine-tuning and fixing bugs with retrieval
- [x] Full install flow (Has been done, but need to test in other environments)
- [x] Testing

Look in aws>slack to see the components of the slack app. READMEs included for each lambda function. Some pipedream workflows as well described in pipedream readme.

## Monday App
- [x] Monday workspace template created
- [x] Monday chatbots integration recipes created
- [ ] Monday documents integration recipes created
- [x] Create a chatbot in monday and then create in supabase
- [x] Update chatbot in monday and update in supabase
- [x] Delete chatbot in monday and delete in supabase and pinecone
- [x] Pull all files from Monday when chatbot is ready to be trained
- [x] Download all files from monday and upload to supabase
- [x] Create pinecone index namespace from files
- [x] Update pinecone index namespace from files 
- [x] Testing

Look in aws>monday to see the components of the monday app. READMEs included for each lambda function. Some pipedream workflows as well described in pipedream readme


## Index Config
In general, this is getting paired down a lot because I am handling a lot with the Monday app and Lambda. Will take small pieces from the current structure
- [x] Receive a trigger to know when an index namespace needs to be trained
- [x] Insert row in chatbot trainings board in monday and keep status up to date
- [x] Process each document as necessary
- [x] As docs processed, update the status on the documents board
- [x] Update the chatbots board with status of complete when done

