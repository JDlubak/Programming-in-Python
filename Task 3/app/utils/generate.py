import random

from sklearn.pipeline import Pipeline

from app.models import Data


def generate_prediction_model() -> Pipeline:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.preprocessing import StandardScaler
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=4, weights="distance"))
    ])
    return model


def generate_points(amount: int = 30, categories_amount: int = 4):
    categories = range(1, categories_amount + 1)
    points = []
    for _ in range(amount):
        point = Data(
            category=random.choice(categories),
            width=round(random.uniform(0.1, 4.0), 2),
            height=round(random.uniform(0.5, 2.0), 2),
            length=round(random.uniform(0.5, 10.0), 2),
            weight=round(random.uniform(0.5, 20.0), 2)
        )
        points.append(point)
    return points
