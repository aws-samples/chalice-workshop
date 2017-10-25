from uuid import uuid4

from chalice import Chalice


app = Chalice(app_name='mytodo')
app.debug = True
_DB = None
DEFAULT_USERNAME = 'default'


class InMemoryTodoDB(object):
    def __init__(self, state=None):
        if state is None:
            state = {}
        self._state = state

    def list_all_items(self):
        all_items = []
        for username in self._state:
            all_items.extend(self.list_items(username))
        return all_items

    def list_items(self, username=DEFAULT_USERNAME):
        return self._state.get(username, {}).values()

    def add_item(self, description, metadata=None, username=DEFAULT_USERNAME):
        if username not in self._state:
            self._state[username] = {}
        uid = str(uuid4())
        self._state[username][uid] = {
            'uid': uid,
            'description': description,
            'state': 'unstarted',
            'metadata': metadata if metadata is not None else {},
            'username': username
        }
        return uid

    def get_item(self, uid, username=DEFAULT_USERNAME):
        return self._state[username][uid]

    def delete_item(self, uid, username=DEFAULT_USERNAME):
        del self._state[username][uid]

    def update_item(self, uid, description=None, state=None,
                    metadata=None, username=DEFAULT_USERNAME):
        item = self._state[username][uid]
        if description is not None:
            item['description'] = description
        if state is not None:
            item['state'] = state
        if metadata is not None:
            item['metadata'] = metadata


def get_app_db():
    global _DB
    if _DB is None:
        _DB = InMemoryTodoDB()
    return _DB


@app.route('/todos', methods=['GET'])
def get_todos():
    return get_app_db().list_items()


# Following the example get_todos() function, add the rest of the required
# routes here...
