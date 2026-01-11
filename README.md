## Programming-in-Python
### Description
[EN]
This repository contains assignments from the course “Programming in 
Python”, taught in English at Technical University of Lodz - 5th 
semester at Applied Computer Science major, Software Engineering and 
Data Analysis specialization. ALL solutions were prepared by myself:
- [@JDlubak](https://github.com/JDlubak)

[PL]
To repozytoriom zawiera zadania z kursu „Programming in 
Python” prowadzonym w języku angielskim na 5 semestrze informatyki 
stosowanej na Politechnice Łódzkiej, na specjalizacji Inżynieria 
oprogramowania i analiza danych. Wszystkie rozwiązywania zostały 
przygotowane przeze 
mnie:
- [@JDlubak](https://github.com/JDlubak)

### Tasks done:

#### Task 1 - Getting familiar with basic data analysis and visualization.

The goal of the project was to practice data analysis 
using the Pandas, Matplotlib, and Seaborn libraries.
Using them, a statistical analysis of the given 
dataset (4177 observations, 9 variables) was performed using Jupyter 
Notebook. The analysis includes:
- frequency and percentage distribution of the qualitative variable ,
- summary statistics for quantitative variables (mean, standard 
  deviation, quartiles, min, max),
- visualizations: bar chart, histograms, scatter plots, and boxplots,
- correlation matrix and its visualization as a heatmap,
- linear regression plot for the most strongly correlated variables,
- summary statistics of quantitative variables grouped by categories 
  of the qualitative variable.

#### Task 2 - Getting familiar with object-oriented programming and the standard library.
This project implements a text-based simulation of a wolf hunting a herd 
of sheep in a limited meadow. The animals move in discrete rounds: 
sheep randomly choose a direction and move, while the wolf always 
targets the nearest sheep and either catches it or moves toward it. 
The program is written in an object-oriented manner and supports saving 
simulation states to JSON and CSV files, visualizing progress through 
console output, and configuring parameters via command-line arguments 
and INI configuration files. Advanced features include logging with 
different severity levels and full validation of user inputs.

#### Task 3 - Getting familiar with web frameworks.
This project implements a web application for collecting and managing 
data used in a machine learning classification task. The application 
stores data points with multiple continuous features and 
one categorical label in a relational database and provides both 
a website and a REST API for adding, viewing, and deleting records. 
The application also includes a k-nearest neighbors (k-NN) 
classifier that, after standardizing features, predicts the most likely 
category for given input values. The system is built using a web 
framework (Flask), a PostgreSQL database, SQLAlchemy as an ORM for 
database access, and scikit-learn for model training and prediction.

