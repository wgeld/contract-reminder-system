# Contract Reminder System

The Contract Reminder System is a tool designed to help users manage and track contract deadlines. It sends reminders via email to ensure that no important dates are missed.

## Features

- **Email Notifications**: Automatically sends email reminders for upcoming contract deadlines.
- **Database Integration**: Stores contract data and reminder history in a database.
- **Configurable Settings**: Customize email settings and reminder intervals.
- **Logging**: Logs system activities for monitoring and debugging.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/contract-reminder-system.git
   cd contract-reminder-system
   ```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r src/requirements.txt
   ```

4. **Configure environment variables**:
   - Copy the `.env.example` to `.env` and fill in the necessary configuration details such as database connection strings and email server settings.

## Usage

1. **Run the main application**:
   ```bash
   python src/main.py
   ```

2. **Check logs**:
   - Logs are stored in `src/script.log` for monitoring the system's activities.

## Configuration

- **Email Settings**: Configure your SMTP server details in the `.env` file.
- **Database Settings**: Ensure your database connection details are correctly set in the `.env` file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

