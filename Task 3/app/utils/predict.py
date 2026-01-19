from typing import List

from sklearn.pipeline import Pipeline

from app.models import Data


def make_prediction(model: Pipeline, db_data: List[Data],
                    form_data: Data) -> int:
    x_train = [[d.width, d.height, d.length, d.weight] for d in db_data]
    y_train = [d.category for d in db_data]

    model.fit(x_train, y_train)

    x_input = [[form_data.width, form_data.height,
                form_data.length, form_data.weight]]
    prediction = model.predict(x_input)
    return int(prediction[0])
