import requests
import base64
import json
import os
from github import Github

# GitHub configuration
github_token = os.environ.get('GITHUB_TOKEN')
github_repo = 'your_username/your_repo'
file_path = 'path/to/your/article.md'

# Medium configuration
medium_token = os.environ.get('MEDIUM_TOKEN')
medium_user_id = 'your_medium_user_id'

def get_github_content(repo, file_path):
    g = Github(github_token)
    repo = g.get_repo(repo)
    file_content = repo.get_contents(file_path)
    return file_content.decoded_content.decode()

def publish_to_medium(title, content, tags):
    url = f'https://api.medium.com/v1/users/{medium_user_id}/posts'
    headers = {
        'Authorization': f'Bearer {medium_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'title': title,
        'contentFormat': 'markdown',
        'content': content,
        'tags': tags,
        'publishStatus': 'draft'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    # Get content from GitHub
    content = get_github_content(github_repo, file_path)
    
    # Extract title from the first line of the content
    title = content.split('\n')[0].lstrip('#').strip()
    
    # Remove the title from the content
    content = '\n'.join(content.split('\n')[1:]).strip()
    
    # You can customize the tags
    tags = ['Programming', 'GitHub', 'Medium']
    
    # Publish to Medium
    result = publish_to_medium(title, content, tags)
    
    if 'data' in result:
        print(f"Article published as draft on Medium: {result['data']['url']}")
    else:
        print("Error publishing to Medium:", result)

if __name__ == '__main__':
    main()
