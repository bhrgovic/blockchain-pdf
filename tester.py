import requests
import time
import os

def main():
    url = 'http://localhost:5001/add_pdf'  # Replace with your actual URL
    email = 'test@example.com'
    file_path = 'blank.pdf'  # Replace with the path to a test PDF file

    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
        data = {'email': email}

     
        # Send 1000 requests
        for i in range(100):
            response = requests.post(url, files=files, data=data)
            if response.status_code != 200:
                print(f"Request {i} failed: {response.text}")
        


    # Calculate and print the total time for all requests
    print(f"Finished")

if __name__ == "__main__":
    main()