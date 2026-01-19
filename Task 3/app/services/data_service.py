from app.db import session
from app.models import Data


def get_all(order_by_category: bool = False) -> list[Data]:
    with session() as s:
        if order_by_category:
            data_points = s.query(Data).order_by(Data.category).all()
        else:
            data_points = s.query(Data).all()
    return data_points


def create_point(point: Data) -> int:
    with session() as s:
        s.add(point)
        s.commit()
        point_id = point.id
    return point_id


def delete_point(point_id: int) -> bool:
    with session() as s:
        point = s.query(Data).filter(Data.id == point_id).first()
        if not point:
            return False
        s.delete(point)
        s.commit()
    return True


def count_points() -> int:
    with session() as s:
        count = s.query(Data).count()
    return count


def initialize_data(points: list[Data]) -> None:
    with session() as s:
        s.add_all(points)
        s.commit()
