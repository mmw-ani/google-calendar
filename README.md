# Google Calendar Integration

-   Get the list of calendar events of your account.

### **How to deploy locally**

-   Clone the repo and open the folder.
-   Create a .env file and paste django token as

    ```
    DJANGO_KEY = "SECRET_KEY"
    ```

-   Generate credentials from google developers and save the file as **credentials.json** in the same folder where manage.py file is located

-   Activate virtual environment
    ```
    	source ./env/bin/activate
    ```
-   Install python dependies
    ```
    pip install -r requirements.txt
    ```
-   Go to the google calendar folder and Start the server
    ```
    python manage.py runserver
    ```
