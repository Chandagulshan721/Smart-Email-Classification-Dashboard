from flask import Flask, render_template
from gmail_service import get_classified_emails

app = Flask(__name__)

# Base Gmail URL to open emails
GMAIL_URL = "https://mail.google.com/mail/u/0/#inbox/"


@app.route("/")
def dashboard():
    # 1️⃣ Fetch classified emails from Gmail
    emails = get_classified_emails(max_results=10)

    # 2️⃣ Attach Gmail clickable URL to each email
    for category, email_list in emails.items():
        for email in email_list:
            email["url"] = GMAIL_URL + email["id"]

    # 3️⃣ Send data to HTML template
    return render_template(
        "dashboard.html",
        data={
            "INTERVIEW": emails.get("INTERVIEW", []),
            "ONLINE JOB": emails.get("ONLINE JOB", []),
            "SOCIAL ADS": emails.get("SOCIAL ADS", [])
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
