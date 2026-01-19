from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app.services import count_points, create_point, delete_point, \
    get_all, initialize_data
from app.utils import (generate_points, make_prediction,
                       validate_point, validate_point_id)

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/data', methods=['GET'])
def get():
    data_points = get_all()
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
    is_valid, result = validate_point(data, for_api=True)
    if not is_valid:
        return {"error": result}, HTTPStatus.BAD_REQUEST
    point = result
    point_id = create_point(point)
    return jsonify({"id": point_id}), HTTPStatus.CREATED


@api_bp.route('/data/<point_id>', methods=['DELETE'])
def delete(point_id):
    is_valid, cause = validate_point_id(point_id)
    if not is_valid:
        return {"error": cause}, HTTPStatus.BAD_REQUEST
    is_found = delete_point(point_id)
    if not is_found:
        return {"error": "Record not found"}, HTTPStatus.NOT_FOUND
    return jsonify({"id": point_id}), HTTPStatus.OK


@api_bp.route('/predictions', methods=['GET'])
def get_prediction():
    data_count = count_points()
    if data_count < 5:
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
    data_points = get_all()
    prediction = make_prediction(data_points, result)
    return jsonify({"predicted_category": prediction}), HTTPStatus.OK


@api_bp.route('/init', methods=['POST'])
def init():
    data_count = count_points()
    if data_count > 0:
        return (jsonify({"error": "Data points are already "
                                  "present in database!"}),
                HTTPStatus.CONFLICT)
    data_points = generate_points()
    initialize_data(data_points)
    return jsonify({"message": "Initialized"}), HTTPStatus.CREATED
