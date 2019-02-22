import requests
from mox_solr_test.config import settings
import re


OS2MO_UI_URL = settings["OS2MO_SERVICE_URL"].rsplit("/service",maxsplit=1)[0]
OS2MO={
    "employee": OS2MO_UI_URL + "/medarbejder/",
    "orgunit": OS2MO_UI_URL + "/organisation/" 
}
FIELDS = {
    "employee": [x["name"] for x in requests.get(settings["SOLR_URL"] + "/solr/os2mo-employee/schema/fields").json()['fields']],
    "orgunit": [x["name"] for x in requests.get(settings["SOLR_URL"] + "/solr/os2mo-orgunit/schema/fields").json()['fields']]
}

def annotate_docs(collection, result):
    os2mo = OS2MO[collection]
    for i in result["response"]["docs"]:
        i["_type"] = collection
        i["_href"] = os2mo + (i["uuid"][0])
        i["_hl"] = result.get("highlighting",{}).get(i["uuid"][0],{})

def lucenequery(collection, params):
    solrpath = settings["SOLR_URL"] + "/solr/os2mo-" + collection + "/select"
    result = requests.get(solrpath, params=params).json()
    annotate_docs(collection, result)
    return result, params
    

def dismaxquery(collection, params, fields=None):
    solrpath = settings["SOLR_URL"] + "/solr/os2mo-" + collection + "/select"
    fields = FIELDS[collection]
    params = dict(params)

    # assume each mentioned field is a regex and 
    # find all fields, that match 
    queryfields = []
    for f in params["qf"].split(" "):
        for qf in fields:
            if re.match(f, qf):
                queryfields.append(qf)

    # make sure that highlighting extends to all the fields matched
    # and make sure that we also search all of these fields
    params["hl.fl"]  = params["qf"] = " ".join(queryfields)
    params["hl.requireFieldMatch"]  = "true"
    result = requests.get(solrpath, params=params).json()
    annotate_docs(collection, result)
    return result, params


def employee_name_options():
    result, params = lucenequery("employee", {"terms": "true", "terms.fl": "name", "terms.limit": -1})
    return "".join(["<option value=\"%s\">%s</option>" %(n,n.title()) for n in sorted(result["terms"]["name"][0::2])])


def department_name_options():
    result, params = lucenequery("orgunit", {"q": "*:*", "fl": "name,uuid,location", "rows": 1000000, })
    return "".join([
        "<option value=\"%s\">%s (%s) </option>" %n 
        for n in [
            (v["uuid"][0], v["name"][0], v.get("location",[""])[0]) 
            for v in  sorted(result["response"]["docs"], key=lambda x: x["name"])
        ]
    ])

def department_children(uuid):
    result, params = dismaxquery("orgunit", {"defType":"dismax", "qf":"(.*parent\.)*uuid", "q":uuid, "fl": "uuid", "rows":1000000 })
    return [v["uuid"][0] for v in result["response"]["docs"]]
    #import pdb; pdb.set_trace()
    


def department_parents(uuid):    
    pass
