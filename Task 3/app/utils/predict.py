from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def make_prediction(db_data, form_data):
    db_values = []
    db_category = []
    for d in db_data:
        db_values.append([d.width, d.height, d.length, d.weight])
        db_category.append(d.category)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("knn", KNeighborsClassifier(n_neighbors=4, weights="distance"))
    ])

    model.fit(db_values, db_category)

    input_data = [[form_data.width, form_data.height,
                   form_data.length, form_data.weight]]
    model_output = model.predict(input_data)
    return int(model_output[0])
