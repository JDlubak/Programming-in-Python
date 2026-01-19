from http import HTTPStatus

from flask import (abort, Blueprint, current_app, redirect,
                   render_template, request, url_for)

from app.services import (count_points, create_point, delete_point,
                          get_all, initialize_data)
from app.utils import (generate_points, make_prediction,
                       validate_point, validate_point_id)

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def home():
    data_points = get_all(order_by_category=True)
    return render_template("home.html", data_points=data_points)


@web_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        input_data = {
            "category": request.form.get('category'),
            "width": request.form.get('width'),
            "height": request.form.get('height'),
            "length": request.form.get('length'),
            "weight": request.form.get('weight')
        }
        valid, result = validate_point(input_data)
        if not valid:
            abort(HTTPStatus.BAD_REQUEST, description=result)
        create_point(result)
        return redirect(url_for('web.home'))
    return render_template("add.html")


@web_bp.route('/delete/<int:point_id>', methods=['POST'])
def delete(point_id):
    is_valid, cause = validate_point_id(point_id)
    if not is_valid:
        abort(HTTPStatus.BAD_REQUEST, description=cause)
    is_found = delete_point(point_id)
    if not is_found:
        abort(HTTPStatus.NOT_FOUND, description="Record not found")
    return redirect(url_for('web.home'))


@web_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    data_count = count_points()
    if data_count < 5:
        abort(HTTPStatus.BAD_REQUEST,
              description="Unable to make prediction; "
                          "Please add more data points to database!"
                          "<br>(At least 5 points required)")
    if request.method == 'POST':
        input_data = {
            "width": request.form.get('width'),
            "height": request.form.get('height'),
            "length": request.form.get('length'),
            "weight": request.form.get('weight')
        }
        valid, result = validate_point(input_data, is_prediction=True)
        if not valid:
            abort(HTTPStatus.BAD_REQUEST, description=result)
        data_points = get_all()
        model = current_app.config['model']
        prediction = make_prediction(model, data_points, result)
        return render_template("prediction_result.html",
                               prediction=prediction)
    return render_template("predict.html")


@web_bp.route('/init', methods=['GET', 'POST'])
def init():
    data_count = count_points()
    if data_count > 0:
        abort(HTTPStatus.CONFLICT, "Data points are already "
                                   "present in database!")
    data_points = generate_points()
    initialize_data(data_points)
    return redirect(url_for('web.home'))
