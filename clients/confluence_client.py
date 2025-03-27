import requests
from requests.auth import HTTPBasicAuth


class ConfluenceClient:
    def __init__(self, url, username, api_token):
        self.url = url
        self.auth = HTTPBasicAuth(username, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def create_page(self, space_id, title, content):
        data = {
            "type": "page",
            "title": title,
            "spaceId": space_id,
            "status": "draft",
            "body": {"storage": {"value": content, "representation": "storage"}},
        }
        response = requests.post(
            f"{self.url}/api/v2/pages",
            headers=self.headers,
            auth=self.auth,
            json=data,
        )
        if response.status_code in [200, 201]:
            print(f"✅ Page '{title}' created!")
            return response.json().get("id")
        else:
            print("❌ Error creating page:", response.text)

        return None

    def delete_page(self, page_id):
        try:
            if self.check_draft(page_id):
                params = {"status": "draft"}
                response = requests.delete(
                    f"{self.url}/rest/api/content/{page_id}",
                    headers=self.headers,
                    auth=self.auth,
                    params=params,
                )
            else:
                response = requests.delete(
                    f"{self.url}/api/v2/pages/{page_id}",
                    headers=self.headers,
                    auth=self.auth,
                )

            if response.status_code in [204, 200]:
                print(f"✅ Page id '{page_id}' deleted!")

            elif response.status_code == 404:
                print(f"Page '{page_id}' already deleted or doesn't exist")
            else:
                print("❌ Error deleting page:", response.text)
        except Exception as e:
            print(f"Error during page deletion: {e}")

    def check_draft(self, page_id):
        response = requests.get(
            f"{self.url}/api/v2/pages/{page_id}",
            headers=self.headers,
            auth=self.auth,
        )
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        return response.json().get("status") == "draft"

    def get_space_id(self, space_key):
        response = requests.get(
            f"{self.url}/rest/api/space",
            headers=self.headers,
            auth=self.auth,
            params={"spaceKey": space_key, "limit": 1},
        )
        if response.status_code == 200:
            results = response.json()["results"]
            if results:
                return results[0]["id"]
            print(f"❌ Space '{space_key}' not found")
            return None
        else:
            print(f"❌ Error accessing Confluence API: {response.text}")

    def get_page_id(self, page_id):
        response = requests.get(
            f"{self.url}/api/v2/pages/{page_id}",
            headers=self.headers,
            auth=self.auth,
        )
        return response.status_code == 200
