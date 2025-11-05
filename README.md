# Setup Instructions

## Backend Setup

Use docker-compose to get the backend up:

```bash
docker-compose up --build -d
```

This will setup the backend with the postgres database image as well.

No need to setup db or seed data as it is already done. If you want to use your own credentials to seed the data update the seed_db.py inside the backend/scripts with your data and credentials.

## Frontend Flutter Setup

1. Install dependencies:
```bash
flutter pub get
```

2. Before running the app, make sure to change the baseUrl in the api_service.dart with your IP address of the machine you have run the backend server on.

3. Run the Flutter app:
```bash
flutter run
```

Make sure to run this on a device before starting the flutter build.