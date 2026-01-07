from http import HTTPStatus

from flask import (abort, Blueprint, redirect,
                   render_template, request, url_for)

from app.db import session
from app.models import Data
from app.utils import make_prediction, validate_point

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def home():
    with session() as s:
        data_points = s.query(Data).all()
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
            abort(HTTPStatus.NOT_FOUND, description=result)
        with session() as s:
            s.add(result)
            s.commit()
        return redirect(url_for('web.home'))
    return render_template("add.html")


@web_bp.route('/delete/<int:point_id>', methods=['POST'])
def delete(point_id):
    with session() as s:
        point = s.query(Data).filter(Data.id == point_id).first()
        if not point:
            abort(HTTPStatus.NOT_FOUND, description="Record not found")
        s.delete(point)
        s.commit()
    return redirect(url_for('web.home'))


@web_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    with session() as s:
        data_points = s.query(Data).all()
    if len(data_points) < 5:
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
            abort(HTTPStatus.NOT_FOUND, description=result)

        prediction = make_prediction(data_points, result)
        return render_template("prediction_result.html",
                               prediction=prediction)
    return render_template("predict.html")
