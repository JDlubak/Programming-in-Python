from http import HTTPStatus

from flask import (abort, Blueprint, redirect,
                   render_template, request, url_for)

from app.db import session
from app.models import Data
from app.utils import validate_point

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
