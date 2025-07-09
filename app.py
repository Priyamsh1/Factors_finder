from flask import Flask, render_template, request, session
from collections import deque

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for session

# Keep only the last 5 results
def update_history(item):
    if 'history' not in session:
        session['history'] = []
    history = deque(session['history'], maxlen=5)
    history.appendleft(item)
    session['history'] = list(history)

def get_factors(n):
    factors = [str(i) for i in range(1, n + 1) if n % i == 0]
    return ", ".join(factors)

def get_prime_factors(n):
    result = []
    for i in range(2, n + 1):
        if n % i == 0:
            is_prime = True
            for j in range(2, i):
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime:
                result.append(str(i))
    return ", ".join(result) if result else f"{n} has no prime factors."

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        number = request.form.get("number")
        operation = request.form.get("operation")
        if number and number.isdigit():
            n = int(number)
            if operation == "factors":
                result = f"Factors of {n}: " + get_factors(n)
            elif operation == "prime_factors":
                result = f"Prime Factors of {n}: " + get_prime_factors(n)
            update_history(result)
        else:
            result = "Please enter a valid positive integer."

    history = session.get('history', [])
    return render_template("index.html", result=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)
