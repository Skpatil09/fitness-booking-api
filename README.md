#  Fitness Studio Booking API

A simple FastAPI backend for managing fitness class schedules and bookings.

##  Features

- View all upcoming fitness classes (Yoga, Zumba, HIIT)
- Book a spot in a class
- View all bookings by email
- Cancel a booking
- Timezone support (classes in IST, can display in any timezone)
- Input validation & error handling

---

## Bonus Features

- Automated Email Reminders: After booking, users receive a confirmation email (mocked—printed in the server console).
- Class Filtering: Users can filter classes by type (name), instructor, or date using query parameters.
- Booking Limits: Each user (email) can book a maximum of 3 classes per week.

##  Project Structure
```
fitness-booking-api/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── load_seed_data.py
├── seed_data.json
├── requirements.txt
└── README.md
```
---

##  Setup Instructions

1. **Unzip the project folder**:

    ```
    cd fitness-booking-api
    ```

2. **Set up a virtual environment**:

    ```
    python -m venv fitness
    # Activate:
    # Windows:
    fitness\Scripts\activate
    # Mac/Linux:
    source fitness/bin/activate
    ```

3. **Install dependencies**:

    ```
    pip install -r requirements.txt
    ```

4. **Load sample data**:

    ```
    python load_seed_data.py
    ```

5. **Run the API server**:

    ```
    uvicorn main:app --reload
    ```

6. **Open the API docs**:

    Visit [http://localhost:8000/docs] in your browser.

---

##  Sample cURL Requests (Try these through normal Command Prompt (not PowerShell)):

### Get all classes

curl -X GET "http://localhost:8000/classes?tz=Asia/Kolkata"

### Filter Classes by Name, Instructor, or Date

curl -X GET "http://localhost:8000/classes?name=Yoga"
curl -X GET "http://localhost:8000/classes?instructor=Anjali"
curl -X GET "http://localhost:8000/classes?date=2025-07-05"
curl -X GET "http://localhost:8000/classes?name=Yoga&date=2025-07-05"

### Book a class

curl -X POST "http://localhost:8000/book"
-H "Content-Type: application/json"
-d '{"class_id": 1, "client_name": "Alice", "client_email": "alice@example.com"}'


For windows:
curl -X POST "http://localhost:8000/book" -H "Content-Type: application/json" -d "{\"class_id\": 1, \"client_name\": \"Alice\", \"client_email\": \"alice@example.com\"}"


### Get bookings by email

curl -X GET "http://localhost:8000/bookings?email=alice@example.com"


### Cancel a booking

curl -X DELETE "http://localhost:8000/booking/1"

---

##  Sample Input Data

See `seed_data.json` for example class entries.

---

##  Testing

You can also use the Swagger UI at [http://localhost:8000/docs] to interact with and test the API in your browser.

---

##  Loom Video Guide

A walkthrough video is included (see below) demonstrating setup, API usage, and key features.
https://www.loom.com/share/5b42cb56fea54eef9ce08d06350623dd?sid=68a2f042-ab54-4d0f-9cd3-1239485d7ba5
---

##  Author

Snehal Patil 
sneh2k@gmail.com


