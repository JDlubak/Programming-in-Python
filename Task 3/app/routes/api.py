from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app.db import session
from app.models import Data
from app.utils import validate_point

api_bp = Blueprint('api', __name__, url_prefix='/api/data')


@api_bp.route('', methods=['GET'])
def get():
    with session() as s:
        data_points = s.query(Data).all()
    result = [
        {
            "id": d.id,
            "width": d.width,
            "height": d.height,
            "length": d.length,
            "weight": d.weight,
            "category": d.category
        }
        for d in data_points
    ]
    return jsonify(result), HTTPStatus.OK


@api_bp.route('', methods=['POST'])
def post():
    is_valid, result = validate_point(request.get_json())
    if not is_valid:
        return {"error": result}, HTTPStatus.BAD_REQUEST
    point = result
    with session() as s:
        s.add(point)
        s.commit()
        point_id = point.id
    return jsonify({"id": point_id}), HTTPStatus.CREATED


@api_bp.route('/<int:point_id>', methods=['DELETE'])
def delete(point_id):
    with session() as s:
        point = s.query(Data).filter(Data.id == point_id).first()
        if not point:
            return {"error": "Record not found"}, HTTPStatus.NOT_FOUND
        s.delete(point)
        s.commit()
    return jsonify({"id": point_id}), HTTPStatus.OK
