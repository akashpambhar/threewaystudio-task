# Audio File Upload and Database Management Application

This is a web application built using Flask for uploading audio files, managing the file database, and checking audio file properties. Users can upload audio files, view their uploaded files, and check for duration limits.

## Features

- User authentication using a username.
- Upload multiple audio files.
- Display a list of uploaded audio files.
- Check if the uploaded audio files exceed the total duration limit.
- Save audio file information in a MySQL database.
- Basic MIME type and duration checks for uploaded files.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python (3.x)
- Flask
- Flask-SQLAlchemy
- Mutagen
- Magic

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
    ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Configure the MySQL database URI in the `app.config['SQLALCHEMY_DATABASE_URI']` line of the `main.py` file. Update the username, password, and database name according to your MySQL setup.

## Usage
1. Run the Flask application: 
    ```bash
    python main.py
    ```

2. Open a web browser and navigate to http://localhost:5000/

3. On the home page, enter your username and submit.

4. You'll be redirected to the file upload page. Upload one or more audio files.

5. The uploaded audio files will be listed on the page along with their details. The application will check if the total duration of uploaded files exceeds the limit.