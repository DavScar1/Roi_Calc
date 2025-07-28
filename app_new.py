from flask import Flask, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.permanent_session_lifetime = timedelta(minutes=30)



@app.route("/", methods=["GET", "POST"])
def roi():
    if request.method == "POST":
        try:
            revenue = round(float(request.form["revenue"]), 2)
            cost = round(float(request.form["cost"]), 2)
            currency = request.form.get("currency", "USD")
            symbol = get_currency_symbol(currency)
            profit = revenue - cost

            if cost <= 0 or revenue < 0:
                message = ("Cost can't be 0 or less or Revenue can't be negative", "error")
                return render_template("newer_results.html", message=message, cost=cost, revenue=revenue, currency=currency, symbol=symbol)

            roi = round((((revenue - cost) / cost) * 100), 2)
            message = ("Calculation successful!", "success")

            calculation = {
                "revenue": float(request.form["revenue"]),
                "cost": float(request.form["cost"]),
                "roi": roi,
                "profit": profit,
                "currency": currency,
                "symbol": symbol
                }

            history = session.get("history", [])
            history.insert(0, calculation)
            session["history"] = history[:3]

            return render_template("newer_results.html", revenue=revenue, cost=cost, profit=profit, roi=roi, currency=currency, symbol=symbol, message=message, history=session.get("history", []))

        except (ValueError, TypeError):
            currency = request.form.get("currency", "USD")
            symbol = get_currency_symbol(currency)
            message = ("Invalid input. Enter numbers only.", "error")
            return render_template("newer_results.html", message=message, currency=currency, symbol=symbol)
    return render_template("new_form.html")

def get_currency_symbol(code):
    return {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }.get(code, "")


if __name__ == "__main__":
    app.run()
