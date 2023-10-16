import requests
import os

def download_file(url, local_filename, access_token=None):
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
    response = requests.get(url, headers=headers, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192): 
            if chunk: 
                f.write(chunk)
    return local_filename


def delete_local_file(path):
    """Delete a file if it exists."""
    try:
        os.remove(path)
        print(f"{path} has been deleted.")
    except FileNotFoundError:
        print(f"{path} not found.")
    except Exception as e:
        print(f"An error occurred while deleting {path}: {e}")