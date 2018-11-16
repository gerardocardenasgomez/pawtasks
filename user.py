import json
import falcon

class Resource(object):
    def on_get(self, req, resp, name):
        doc = {"user":"hi, {0}".format(name)}

        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200
