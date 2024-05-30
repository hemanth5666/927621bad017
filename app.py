from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

window_size = 10
stored_numbers = []

def generate_numbers():
    return [random.randint(1, 100) for _ in range(10)]

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def filter_numbers(number_list, qualifier):
    filtered_numbers = []
    for num in number_list:
        if qualifier == 'p':
            if is_prime(num):
                filtered_numbers.append(num)
        elif qualifier == 'f':
            if is_fibonacci(num):
                filtered_numbers.append(num)
        elif qualifier == 'e':
            if num % 2 == 0:
                filtered_numbers.append(num)
        elif qualifier == 'o':
            if num % 2 != 0:
                filtered_numbers.append(num)
    return filtered_numbers

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    if n < 0:
        return False
    a, b = 0, 1
    while a < n:
        a, b = b, a + b
    return a == n

@app.route("/numbers/<qualifier>", methods=["GET"])
def get_numbers(qualifier):
    global stored_numbers
    start_time = time.time()
    
    numbers_from_server = generate_numbers()
    stored_numbers += numbers_from_server
    stored_numbers = list(set(stored_numbers))  

    filtered_numbers = filter_numbers(stored_numbers, qualifier)

    if len(stored_numbers) > window_size:
        stored_numbers = stored_numbers[-window_size:]

    avg = calculate_average(stored_numbers[-window_size:])

    end_time = time.time()

    response = {
        "windowPrevState": stored_numbers[:-len(numbers_from_server)],
        "windowCurrState": stored_numbers[-len(numbers_from_server):],
        "numbers": filtered_numbers,
        "avg": "{:.2f}".format(avg),
        "responseTime": "{:.2f}".format((end_time - start_time) * 1000)  # Response time in milliseconds
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
