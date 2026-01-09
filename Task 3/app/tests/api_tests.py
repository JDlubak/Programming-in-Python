import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.environ.get('BASE_URL')


def print_result(response):
    print(f'Status code: {response.status_code}')
    try:
        print(f'Response JSON:\n{response.json()}')
    except requests.exceptions.JSONDecodeError:
        print(f'Error while decoding response error: {response.text}')


def get_data_test():
    url = f'{BASE_URL}/data'
    response = requests.get(url)
    print_result(response)


def post_data_test():
    url = f'{BASE_URL}/data'
    width = input("Width: ")
    height = input("Height: ")
    length = input("Length: ")
    weight = input("Weight: ")
    category = input("Category: ")
    params = {
        "width": width,
        "height": height,
        "length": length,
        "weight": weight,
        "category": category
    }
    response = requests.post(url, json=params)
    print_result(response)


def delete_data_test():
    point_id = input("Id of data point to delete: ")
    url = f'{BASE_URL}/data/{point_id}'
    response = requests.delete(url)
    print_result(response)


def get_predictions_test():
    url = f'{BASE_URL}/predictions'
    width = input("Width: ")
    height = input("Height: ")
    length = input("Length: ")
    weight = input("Weight: ")
    params = {
        "width": width,
        "height": height,
        "length": length,
        "weight": weight
    }
    response = requests.get(url, params=params)
    print_result(response)


def init_test():
    url = f'{BASE_URL}/init'
    response = requests.post(url)
    print_result(response)


def main_menu():
    while True:
        print('Please select API method to be tested: ')
        print('1 - GET /api/data')
        print('2 - POST /api/data')
        print('3 - DELETE /api/data<record_id>')
        print('4 - GET /api/predictions')
        print('5 - POST /api/init')
        choice = input('Your choice: ')
        if choice == '1':
            method = get_data_test
        elif choice == '2':
            method = post_data_test
        elif choice == '3':
            method = delete_data_test
        elif choice == '4':
            method = get_predictions_test
        elif choice == '5':
            method = init_test
        else:
            print('Invalid choice')
            method = None
        if method is not None:
            print('---------------------------------------------------')
            try:
                method()
            except requests.exceptions.ConnectionError:
                print('Connection error: could not connect to the '
                      'server!')
            except requests.exceptions.Timeout:
                print('Timeout error: server did not respond in time!')
            except Exception as e:
                print(f'Unexpected error: {e}')
            print('---------------------------------------------------')


main_menu()
