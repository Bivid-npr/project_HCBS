# Horizon Cinema Booking System

A desktop cinema booking system built with Python, PyQt6, PostgreSQL, and an MVC-style project structure. The application supports role-based login, cinema and screen management, film listings, seat selection, ticket booking, booking cancellation, pricing policies, receipts, and management reports.

## Features

- Role-based authentication for booking staff, admins, and managers
- Film management with listings by screen, date, and show time
- Cinema, city, screen, and seat configuration
- Seat availability checks and visual seat selection workflow
- Pricing by city, show time, and seat type
- Customer creation and booking reference generation
- Booking cancellation with refund calculation
- Reports for bookings, revenue, top films, and staff performance
- PostgreSQL schema and seed data included in `project_HCBS/database_dump.sql`
- Pytest test coverage for core model and pricing behavior

## Tech Stack

- Python 3
- PyQt6
- PostgreSQL
- psycopg2
- python-dotenv
- pytest

## Project Structure

```text
project_HCBS/
  controller/        Application logic and database operations
  db/                PostgreSQL connection helper
  models/            Domain models and enums
  tests/             Pytest test suite
  view/              PyQt6 user interface screens and dialogs
  database_dump.sql  Database schema, views, and sample data
  main.py            Application entry point
  requirements.txt   Python dependencies
  pytest.ini         Test configuration
```

## Setup

1. Create and activate a virtual environment.

```bash
cd project_HCBS
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database.

```sql
CREATE DATABASE horizon_cinema;
```

4. Import the database dump.

```bash
psql -U postgres -d horizon_cinema -f database_dump.sql
```

5. Create a `.env` file inside `project_HCBS`.

```env
DB_HOST=localhost
DB_NAME=horizon_cinema
DB_USER=postgres
DB_PASSWORD=your_password_here
```

Update the values to match your local PostgreSQL setup.

## Running the Application

From inside the `project_HCBS` directory, run:

```bash
python main.py
```

The application opens at the login screen.

## Running Tests

From inside the `project_HCBS` directory, run:

```bash
pytest
```

The test configuration is defined in `pytest.ini`, and tests are located in `tests/`.

## Main Modules

- `main.py` starts the PyQt6 application and opens `LoginView`.
- `db/connection.py` loads database settings from `.env` and creates PostgreSQL connections.
- `controller/auth_controller.py` handles password hashing, login, and staff/admin registration.
- `controller/booking_controller.py` handles seat availability, pricing, customers, bookings, receipts, and booking references.
- `controller/cancellation_controller.py` handles booking cancellation and refund calculation.
- `controller/cinema_controller.py` handles city, cinema, screen, seat, and pricing configuration.
- `controller/film_controller.py` handles films, listings, listing conflicts, and listing updates.
- `controller/report_factory.py` builds reports from PostgreSQL views.
- `models/` contains the core domain objects such as `Cinema`, `Screen`, `Seat`, `Film`, `Listing`, `Booking`, `Customer`, and enums.
- `view/` contains the PyQt6 screens for admins, managers, booking staff, login, and seat selection.

## Database Notes

The included SQL dump defines the main tables:

- `users`
- `city`
- `cinema`
- `screen`
- `seat`
- `film`
- `listing`
- `customer`
- `booking`
- `booking_seat`
- `receipt`
- `pricing_policy`

It also defines reporting views used by the manager/admin reporting features:

- `report_bookings_per_listing`
- `report_monthly_revenue`
- `report_staff_performance`
- `report_top_revenue_film`

## Notes for Development

- Keep database credentials in `.env`; do not hard-code them in source files.
- Run `pytest` after changing model, pricing, booking, or controller logic.
- When adding new database-dependent features, update `database_dump.sql` if the schema changes.
- The application expects PostgreSQL enum values to match the enum values defined in `models/enums.py`.
