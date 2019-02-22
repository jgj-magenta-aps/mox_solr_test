import flask
import requests
from flask import Flask
from mox_solr_test.config import settings
from mox_solr_test import queries, frontpage, resultpage, multiqueries
import re


app = Flask(__name__)


@app.route('/')
def solr_test_single():
    """ single query - only goes so far - and there is no apparent way to make joins
    """
    if flask.request.args.get("q"):

        # we have two collections (employee/orgunit - must be in in args)
        # both solrpath and path to document in os2mo depends on that
        collection = flask.request.args.get("collection")
        os2mo = queries.OS2MO[collection]
        solrurl = settings["SOLR_URL"] + "/solr/os2mo-" + collection + "/select" 

        if flask.request.args.get("defType","") == "dismax":
            # for searching multiple fields without 'catch-all/copy fields'
            # we need a dismax-query with 'qf': query-fields.
            # see dismaxquery example above on how to have field-wildcards
            result, params = queries.dismaxquery(collection, flask.request.args, FIELDS[collection])
        else:
            # a normal one-field-query is a lucene-query
            result, params = queries.lucenequery(collection, flask.request.args)
        return resultpage.render(flask.request.args, params, result, solrurl)
    else:
        return frontpage.render()

@app.route('/multi/')
def solr_test_multiple():
    """ multiple queries
    """
    if flask.request.args.get("multiquery"):
        result, params = multiqueries.multiqueries[flask.request.args.get("multiquery")](flask.request.args)
        return resultpage.render(flask.request.args, params, result, "")
    else:
        return multiqueries.render()

if __name__ == '__main__':
    app.run(host="0.0.0.0")
