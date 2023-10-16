import requests

MONDAY_URL = 'https://api.monday.com/v2'

def get_boards_in_workspace(access_token: str, workspace_id: int):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    if not workspace_id:
        workspace_id = "null"
    query = f'''
        query {{
            boards (workspace_ids: {workspace_id}) {{
                name
                id
                board_folder_id
                columns {{
                    id
                    title
                }}
            }}
        }}
    '''
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        boards = r_json['data']['boards']
        print(boards)
        return boards
    except:
        print(f'Could not convert response into json, returning current api request {r.text}')
        return None
    
def get_board_ids_for_account(boards):
    documents_id, usage_id, trainings_id = None, None, None
    for board in boards:
        if board['name'] == 'Documents':
            for column in board['columns']:
                if column['id'] == 'long_text' and column['title'] == 'Error Message':
                    documents_id = board['id']
                    break
        elif board['name'] == 'Usage':
            for column in board['columns']:
                if column['id'] == 'long_text' and column['title'] == 'Prompt':
                    usage_id = board['id']
                    break
        elif board['name'] == 'Chatbot Trainings':
            for column in board['columns']:
                if column['id'] == 'long_text' and column['title'] == 'Message':
                    trainings_id = board['id']
                    break
    return documents_id, usage_id, trainings_id

get_boards_in_workspace(access_token='eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI3NDYwNDY3MCwiYWFpIjoxMSwidWlkIjo0NTY4MTk0MywiaWFkIjoiMjAyMy0wOC0xMVQxNzowMjoyMy41MzZaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTc4MTEwMDYsInJnbiI6InVzZTEifQ.RLJI3-g4CwGUBMW7RuuuytX8tPhhIloTO-2obvWe8y8', workspace_id=None)