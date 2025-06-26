import sqlite3
from datetime import date, timedelta, datetime
from send_email import send_automated_email

def send_reminder_emails():
    # Connect to the database
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()

    # Get the current date
    today = date.today()

    # Retrieve all reminders from the database
    cursor.execute("SELECT id, title, description, first_reminder_date, reminder_frequency FROM reminders")
    reminders = cursor.fetchall()

    for reminder in reminders:
        reminder_id, title, description, first_reminder_date, reminder_frequency = reminder

        # Convert the first_reminder_date to a date object using datetime.strptime()
        first_reminder_date = datetime.strptime(first_reminder_date, "%Y-%m-%d").date()


        # Check if the current date matches the reminder date based on the frequency
        if reminder_frequency == "Daily":
            days_since_first = (today - first_reminder_date).days
            if days_since_first >= 0:
                send_reminder_email(reminder_id, title, description)
        elif reminder_frequency == "Weekly":
            days_since_first = (today - first_reminder_date).days
            if days_since_first >= 0 and days_since_first % 7 == 0:
                send_reminder_email(reminder_id, title, description)
        elif reminder_frequency == "Monthly":
            if today.day == first_reminder_date.day:
                send_reminder_email(reminder_id, title, description)
        elif reminder_frequency == "Yearly":
            if today.month == first_reminder_date.month and today.day == first_reminder_date.day:
                send_reminder_email(reminder_id, title, description)

    # Close the database connection
    conn.close()

def send_reminder_email(reminder_id, title, description):
    # Construct the email subject and body
    subject = title
    greeting = f"Dear Wes Elliott,\n\n"
    body_text = f"Here is your reminder:\n\n{description}\n\n"
    conclusion = "Regards,\nJarvis"
    body = greeting + body_text + conclusion

    # Send the email
    send_automated_email("your_email@example.com", subject, body)

    print(f"Reminder email sent successfully for reminder ID {reminder_id}.")
