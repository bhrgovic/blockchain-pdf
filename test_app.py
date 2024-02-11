import requests

def send_pdf_to_server(url, file_path, email):
    """
    Sends a PDF file to the server.

    :param url: URL of the endpoint (e.g., 'http://<server-ip>:<port>/add_pdf')
    :param file_path: Path to the PDF file to upload.
    :param email: Email associated with the PDF.
    """
    files = {'file': open(file_path, 'rb')}
    data = {'email': email}

    response = requests.post(url, files=files, data=data)

    return response

# Example usage
if __name__ == "__main__":
    url = 'http://localhost:5000/add_pdf'
    file_path = '/blank.pdf'  # Update this path
    email = 'pi3@test.com'

    response = send_pdf_to_server(url, file_path, email)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")