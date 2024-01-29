from re import M
from flask import Blueprint, request
from ..elastic.elasticClient import ElasticClient

bp = Blueprint("search", __name__)

elastic = ElasticClient()
@bp.route("/search")
def get_post():
    """Search for files with certain content"""
    return elastic.search(request.args.get('txt'))





