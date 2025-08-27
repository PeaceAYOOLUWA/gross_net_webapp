from flask import Flask, render_template, request, send_file
import sqlite3
import csv
from datetime import datetime

app = Flask(__name__)
DB_NAME = "salary.db"

# Tax Band Calculation
def calculate_tax_bands(taxable_income):
    bands = [
        (300000, 0.07),
        (300000, 0.11),
        (500000, 0.15),
        (500000, 0.19),
        (1600000, 0.21),
        (3200000, 0.24)
    ]
    total_tax = 0
    remaining = taxable_income
    band_details = []

    for limit, rate in bands:
        if remaining <= 0:
            break
        amount_taxed = min(remaining, limit)
        tax = amount_taxed * rate
        band_details.append((amount_taxed, rate, tax))
        total_tax += tax
        remaining -= amount_taxed

    return total_tax, band_details

#  Database structure Help 
def save_salary(gross, annual_pension, annual_tax, monthly_net):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO salaries (gross, pension, tax, net, created_at) VALUES (?, ?, ?, ?, ?)",
        (gross, annual_pension, annual_tax, monthly_net, datetime.now())
    )
    conn.commit()
    conn.close()

def get_all_salaries():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM salaries ORDER BY created_at ASC")
    rows = c.fetchall()
    conn.close()
    return rows

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    breakdown = None
    print("Refreshing Page...")
    if request.method == "POST":
        try:
            gross = float(request.form["gross"].replace(",", ""))
        except ValueError:
            return render_template("index.html", error="Invalid input. Please enter a valid number.")

        # Pension & CRA calculations
        annual_gross = gross * 12
        annual_pension = 0.08 * annual_gross
        cra1 = annual_gross - annual_pension
        cra2 = (0.2 * cra1) + 200000
        taxable_income = max(0, cra1 - cra2)

        annual_tax, tax_bands = calculate_tax_bands(taxable_income)
        monthly_pension = annual_pension / 12
        monthly_tax = annual_tax / 12
        monthly_net = gross - (monthly_pension + monthly_tax)

        # Save to DB
        save_salary(gross, annual_pension, annual_tax, monthly_net)

        breakdown = {
            "gross": gross,
            "annual_gross": annual_gross,
            "annual_pension": annual_pension,
            "cra1": cra1,
            "cra2": cra2,
            "taxable_income": taxable_income,
            "annual_tax": annual_tax,
            "monthly_pension": monthly_pension,
            "monthly_tax": monthly_tax,
            "monthly_net": monthly_net,
            "tax_bands": tax_bands
        }

    return render_template("index.html", breakdown=breakdown)

@app.route("/history")
def history():
    salaries = get_all_salaries()
    return render_template("history.html", salaries=salaries)

@app.route("/export_local")
def export_local():
    salaries = get_all_salaries()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"salary_history_{timestamp}.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Gross", "Annual Pension", "Annual Tax", "Monthly Net", "Date"])
        for row in salaries:
            writer.writerow(row)

    return f"CSV exported locally to {file_path}"

if __name__ == "__main__":
    app.run(debug=True, port=5500)
