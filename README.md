[![CircleCI](https://circleci.com/gh/edvm/Django-Gym-Member-Manager/tree/dev.svg?style=svg)](https://circleci.com/gh/edvm/Django-Gym-Member-Manager/tree/dev)

# Django-Gym-Member-Manager
A Gym Member Manager Web App using Django

A simple gym member manager to keep a track of all payments and members

## Features

- Easy to use (Even an amateur can use!)
- A simple GUI
- Faster load speeds (thanks to Django 2.0!)
- Reports for keeping track of payments and admissions

## How to use

- Download the zip
- Extract the contents
- Install all dependencies by executing the following command:

    ```
    $pip install -r requirements.txt
    ```

- For running the application simply execute the following commands:

    ```
    $python3 manage.py migrate
    $python3 manage.py runserver
    ```

- For creating a user execute:

    ```
    $python3 manage.py createsuperuser
    # Follow the instructions
    ```

- You can now login to the system!
