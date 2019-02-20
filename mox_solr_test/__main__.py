import flask
import requests
from flask import Flask
from mox_solr_test.config import settings
from mox_solr_test import frontpage, resultpage
import re


app = Flask(__name__)

OS2MO_UI_URL = settings["OS2MO_SERVICE_URL"].rsplit("/service",maxsplit=1)[0]
OS2MO={
    "employee": OS2MO_UI_URL + "/medarbejder/",
    "orgunit": OS2MO_UI_URL + "/organisation/" 
}
FIELDS = {
    "employee": [x["name"] for x in requests.get(settings["SOLR_URL"] + "/solr/os2mo-employee/schema/fields").json()['fields']],
    "orgunit": [x["name"] for x in requests.get(settings["SOLR_URL"] + "/solr/os2mo-orgunit/schema/fields").json()['fields']]
}


def lucenequery(solrpath, params):
    return requests.get(solrpath, params=params).json()
    

def dismaxquery(solrpath, params, fields):
    params = dict(params)
    queryfields = []
    for f in params["qf"].split(" "):
        for qf in fields:
            if re.match(f, qf):
                queryfields.append(qf)
    params["hl.fl"]  = params["qf"] = " ".join(queryfields)
    params["hl.requireFieldMatch"]  = "true"
    #print(params)
    return requests.get(solrpath, params=params).json()


@app.route('/')
def solr_test():
    if flask.request.args.get("q"):
        q = flask.request.args["q"]
        collection = flask.request.args.get("collection")
        os2mo = OS2MO[collection]
        solrpath = settings["SOLR_URL"] + "/solr/os2mo-" + collection + "/select"
        if flask.request.args.get("defType","") == "dismax":
            result = dismaxquery(solrpath, flask.request.args, FIELDS[collection])
        else:
            result = lucenequery(solrpath, flask.request.args)
        for i in result.get("response",{}).get("docs",[]):
            i["_type"] = collection
            i["_href"] = os2mo + (i["uuid"][0])
            i["_hl"] = result.get("highlighting",{}).get(i["uuid"][0],{})
        return resultpage.render(q, result)
    else:
        return frontpage.render()



if __name__ == '__main__':
    app.run(host="0.0.0.0")
