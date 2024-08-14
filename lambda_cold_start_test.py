import boto3
import time
from datetime import datetime

lambda_client = boto3.client('lambda')

def invoke_lambda(function_name):
    start_time = datetime.now()
    response = lambda_client.invoke(FunctionName=function_name)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() * 1000
    print(f"Function: {function_name}, Duration: {duration:.2f}ms, Response: {response['StatusCode']}")
    return duration

def cold_start_test(function_names, iterations=100):
    durations = {name: [] for name in function_names}
    
    for i in range(iterations):
        print(f"Starting iteration {i+1}/{iterations}...")
        for function_name in function_names:
            print(f"Invoking {function_name}...")
            duration = invoke_lambda(function_name)
            durations[function_name].append(duration)
        
        # Sleep for 10 minutes after invoking all functions
        sleep_seconds = 600 # 10 minutes
        # print what time is actually set in the sleep_seconds variables
        print(f"Sleeping for {sleep_seconds} seconds...")
        time.sleep(sleep_seconds) 
        print("Waking up from sleep...")

    return durations

def generate_function_names(base_names, count=10):
    function_names = []
    for base in base_names:
        # start from i=1 to avoid the base name itself
        for i in range(1, count):
            function_names.append(f"{base}{i}perf")
    return function_names

if __name__ == "__main__":
    # Define base names and how many variations you expect (e.g., current, current1, bottlecap, bottlecap1)
    base_function_names = ["current", "bottlecap"]
    function_names = generate_function_names(base_function_names, count=10)  # Generate names like current, current1, etc.
    
    # Run the cold start test
    durations = cold_start_test(function_names, iterations=100)
    
    # Calculate and print average durations for each function
    for function_name, times in durations.items():
        if times:  # Check if there are recorded durations
            print(f"{function_name.capitalize()} Average Duration: {sum(times)/len(times):.2f} ms")
        else:
            print(f"No successful invocations for {function_name}.")
