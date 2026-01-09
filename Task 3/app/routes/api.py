from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app.db import session
from app.models import Data
from app.utils import generate_points, make_prediction, validate_point

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/data', methods=['GET'])
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


@api_bp.route('/data', methods=['POST'])
def post():
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Missing JSON!"}, HTTPStatus.BAD_REQUEST
    is_valid, result = validate_point(request.get_json(), for_api=True)
    if not is_valid:
        return {"error": result}, HTTPStatus.BAD_REQUEST
    point = result
    with session() as s:
        s.add(point)
        s.commit()
        point_id = point.id
    return jsonify({"id": point_id}), HTTPStatus.CREATED


@api_bp.route('/data/<point_id>', methods=['DELETE'])
def delete(point_id):
    try:
        point_id = int(point_id)
    except ValueError:
        return ({"error": "Invalid id, must be a positive integer"},
                HTTPStatus.BAD_REQUEST)
    with session() as s:
        point = s.query(Data).filter(Data.id == point_id).first()
        if not point:
            return {"error": "Record not found"}, HTTPStatus.NOT_FOUND
        s.delete(point)
        s.commit()
    return jsonify({"id": point_id}), HTTPStatus.OK


@api_bp.route('/predictions', methods=['GET'])
def get_prediction():
    with session() as s:
        data_points = s.query(Data).all()
    if len(data_points) < 5:
        return ({"error": "Unable to make prediction; "
                          "Please add more data points to database! "
                          "(At least 5 points required)"},
                HTTPStatus.BAD_REQUEST)
    input_data = {
        'width': request.args.get('width'),
        'height': request.args.get('height'),
        'length': request.args.get('length'),
        'weight': request.args.get('weight')
    }
    is_valid, result = validate_point(input_data, is_prediction=True,
                                      for_api=True)
    if not is_valid:
        return {"error": result}, HTTPStatus.BAD_REQUEST
    prediction = make_prediction(data_points, result)
    return jsonify({"predicted_category": prediction}), HTTPStatus.OK


@api_bp.route('/init', methods=['POST'])
def init():
    with session() as s:
        if s.query(Data).count() > 0:
            return (
                jsonify({"error": "Data points are already "
                                  "present in database!"}),
                HTTPStatus.CONFLICT
            )
        data_points = generate_points()
        s.add_all(data_points)
        s.commit()
    return jsonify({"message": "Initialized"}), HTTPStatus.CREATED
