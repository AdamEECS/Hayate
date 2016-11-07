import json


_session = {}


def save_session():
    with open('session.json', 'w') as f:
        s = json.dumps(_session, indent=2)
        f.write(s)


def load_session():
    with open('session.json', 'r') as f:
        # s = json.dumps(_session, indent=2)
        s = f.read()
        # _session = json.loads(s)
        _session.update(json.loads(s))


def session(key, value=None):
    if value is None:
        return _session.get(key)
    else:
        _session[key] = value
        save_session()
