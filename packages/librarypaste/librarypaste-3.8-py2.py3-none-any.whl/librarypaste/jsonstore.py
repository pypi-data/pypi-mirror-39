import re
import os
import time
import datetime
import json

from .datastore import DataStore


class JsonDataStore(DataStore):
    """Stores using json encoded into files"""

    def __init__(self, repo):
        super(JsonDataStore, self).__init__()
        self.repo = repo
        if not os.path.exists(repo):
            os.mkdir(repo)
        self.shortids = {}

    def _store(self, uid, content, data=None):
        content['time'] = time.mktime(content['time'].timetuple())
        with self.open(uid, mode='w') as fd:
            json.dump(content, fd)
        if data:
            with self.open('%s.raw' % uid, mode='wb') as fd:
                fd.write(data)
        try:
            self.shortids[content['shortid']] = uid
            sid = '%s %s\n' % (content['shortid'], uid)
            with self.open('shortids.txt', mode='a') as short_id_file:
                short_id_file.write(sid)
        except KeyError:
            pass

    def _storeLog(self, nick, time, uid):
        with self.open('log.txt', mode='a') as f:
            f.write('%s %s\n' % (nick, uid))

    def open(self, filename, *args, **kwargs):
        path = os.path.join(self.repo, filename)
        return open(path, *args, **kwargs)

    def load_key_values(self, filename):
        lines = (
            line.strip().partition(' ')
            for line in self.open(filename)
        )
        return {
            key: value
            for key, sep, value in lines
        }

    def lookup(self, nick):
        return self.load_key_values('log.txt').get(nick)

    def _lookupUid(self, shortid):
        if shortid not in self.shortids:
            self.shortids = self.load_key_values('shortids.txt')
        return self.shortids.get(shortid)

    def _retrieve(self, uid):
        with self.open(uid) as f:
            val = f.read()
        if not val:
            raise ValueError("empty paste")
        paste = json.loads(val)
        if paste.get('type', None) == 'file':
            with self.open('%s.raw' % uid, mode='rb') as f:
                paste['data'] = f.read()
        paste.setdefault('type', 'file' if paste.get('data') else 'code')
        paste['time'] = datetime.datetime.fromtimestamp(paste['time'])
        return paste

    def _delete(self, uid):
        os.remove(os.path.join(self.repo, uid))
        data_fn = os.path.join(self.repo, '%s.raw' % uid)
        os.path.exists(data_fn) and os.remove(data_fn)
        # todo: delete any shortid

    def list(self):
        uid_pattern = re.compile(
            '^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$')
        return map(uid_pattern.match, os.listdir(self.repo))
