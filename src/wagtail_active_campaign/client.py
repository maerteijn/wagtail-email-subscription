from activecampaign import client


class Client(client.Client):
    configured = False

    SUBSCRIBED = 1
    UNSUBSCRIBED = 2

    def __init__(self, url, api_key):
        if url and api_key:
            self.configured = True
            super().__init__(url, api_key)

    def check_credentials(self):
        if not self.configured:
            return False

        response = self.lists.retrieve_all_lists()
        if isinstance(response, str) and len(response) == 0:
            return False
        return True

    def get_list_choices(self):
        # TODO: Check for nr of results and do as much lookups as needed, or implement
        # pagination
        response = self.lists.retrieve_all_lists(limit=100)
        return response["lists"]

    def create_or_update_contact(self, data):
        post_data = {"contact": data}
        response = self.contacts.create_or_update_contact(post_data)
        return response["contact"]

    def add_contact_to_list(self, contact_id, list_id):
        post_data = {
            "contactList": {
                "list": list_id,
                "contact": contact_id,
                "status": self.SUBSCRIBED,
            }
        }
        response = self.contacts.update_list_status_for_a_contact(post_data)
        return response["contactList"]
