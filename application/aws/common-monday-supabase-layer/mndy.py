import requests
import json
import logging

MONDAY_URL = 'https://api.monday.com/v2'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) 

def get_item(access_token, item_id):  
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    
    item_query = f"""
        query {{
            items (ids: {item_id}) {{
                name
                column_values {{
                    id
                    title
                    value
                    text
                    type
                }}
            }}
        }}
    """
    data = {'query': item_query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        return r_json
    except:
        print(f'Could not convert response into json when getting item: {item_id} \nError: {r.text}')
        return None


def update_group_name(access_token, board_id, group_id, new_group_title):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    group_name = str(new_group_title).strip()
    query = f"""
        mutation {{
            update_group (board_id: {board_id}, group_id: "{group_id}", group_attribute: title, new_value: "{group_name}" ) {{
                id
            }}
        }}
    """
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        return r_json['data']['update_group']['id']
    except:
        print(f'Could not convert response into json when creating group: {group_name} for board: {board_id}')
        return None
    

def get_groups_from_board(access_token, board_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f"""
        query {{
            boards (ids: {board_id}) {{
                groups {{
                    title
                    id
                }}
            }}
        }}
    """
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        return r_json
    except:
        print(f'Could not convert response into json when getting groups from board: {board_id}')
        return None


def create_group_in_board(access_token, board_id, group_name):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    group_name = str(group_name)
    query = f"""
        mutation {{
            create_group (board_id: {board_id}, group_name: "{group_name}" ) {{
                id
            }}
        }}
    """
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        return r_json['data']['create_group']['id']
    except:
        print(f'Could not convert response into json when creating group: {group_name} for board: {board_id} \nError: {r.text}')
        return None
    

def send_error(access_token, board_id, item_id, message):
    pass


def delete_item(access_token, item_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f"""
        mutation {{
            delete_item (item_id: {item_id} ) {{
                id
            }}
        }}
    """
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )

    try:
        r_json = r.json()
        return r_json
    except:
        print(f'Could not delete: {r.text}')
        return None


def delete_group(access_token, board_id, group_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f"""
        mutation {{
            delete_group (board_id: {board_id}, group_id: "{group_id}" ) {{
                id
            }}
        }}
    """
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )

    try:
        r_json = r.json()
        return r_json
    except:
        print(f'Could not delete: {r.text}')
        return None
    

def get_item_values_and_assets(access_token, item_ids: list[int]):
    """
    Gets all the item values from a given dictionary of board ids to its correspondings
    item ids

    Args:
        config (dict): Basic config variables
        id_map (list): List of dicts {board ids : [item ids]}

    Returns:
        values (list): All the item values
    """   
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    values = {}
    page = 1
    has_more = True
    limit = 100
    while has_more:
        query = f'''
            query {{
                items (limit:{limit}, page:{page} ids:{item_ids}) {{
                    id
                    name
                    group {{
                        id
                        title
                    }}
                    column_values {{
                        id
                        title
                        value
                        text
                        type
                    }}
                    assets {{
                        id
                        name
                        url,
                        public_url
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
        except:
            print(f'Could not convert response into json, returning current list of values if any, {values} \nError: {r.text}')
            return values
        if 'data' not in r_json:
            return values
        for item in r_json['data']['items']:
            columns = []
            for column in item['column_values']:
                columns.append(column)
            values[item['id']] = {
                'name': item.get('name'),
                'group': item.get('group'),
                'column_values': columns,
                'assets': item.get('assets')
            }
        
        if r_json['data']['items'] and len(r_json['data']['items']) == 100:
            page += 1
        else:
            has_more = False
    return values

def get_item_ids(access_token: str, board_id: int):
    page = 1
    has_more = True
    ids = set()
    limit = 100
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    while has_more:
        query = f'''
            query {{
                boards (ids: {board_id}) {{
                    items (limit:{limit}, page:{page}) {{
                        id
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
        except:
            print(f'Could not convert response into json, returning current list of ids if any, {ids} \nError: {r.text}')
            return ids
        if 'data' not in r_json:
            return ids
        if not r_json['data']['boards']:
            has_more = False
            continue
        for item in r_json['data']['boards'][0]['items']:
            ids.add(int(item['id']))

        if r_json['data']['boards'][0]['items'] and len(r_json['data']['boards'][0]['items']) == limit:
            page += 1
        else:
            has_more = False
    return list(ids)


def update_item(access_token, board_id, item_id, column_values):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f"""
        mutation {{
            change_multiple_column_values (item_id: {item_id}, board_id: {board_id}, column_values: {column_values} ) {{
                id
            }}
        }}
    """
    data = {'query': query}
    r = requests.post(
        url=MONDAY_URL,
        headers=headers,
        json=data
    )
    try:
        r_json = r.json()
        return r_json
    except:
        print(f'Could not convert response into json when updating column values: {r.text}')
        return None
    
def get_board_folder_and_workspace(access_token: str, board_id: int):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f'''
        query {{
            boards (ids: {board_id}) {{
                name
                board_folder_id
                workspace_id
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
        board = r_json['data']['boards'][0]
        return board['board_folder_id'], board['workspace_id']
    except:
        print(f'Could not convert response into json, returning current api request {r.text}')
        return None, None
    
def get_boards_in_workspace(access_token: str, workspace_id: int | None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    if workspace_id is None:
        workspace_id = "null"
    logger.info(workspace_id)
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
        return boards
    except:
        logger.error(f'[mndy common layer]: ERROR : Could not convert response into json, returning current api request {r.text}')
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

def create_item(access_token: str, board_id: str, item_name: str, column_values: dict):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f'''
        mutation {{
            create_item (board_id: {board_id}, item_name: "{item_name}", column_values: {json.dumps(json.dumps(column_values))} ) {{
                id
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
        return r_json
    except:
        print(f'Could not convert response into json, returning current api request {r.text}')
        return None
    
def create_item_no_values(access_token: str, board_id: str, item_name: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    query = f'''
        mutation {{
            create_item (board_id: {board_id}, item_name: "{item_name}" ) {{
                id
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
        return r_json
    except:
        print(f'Could not convert response into json, returning current api request {r.text}')
        return None