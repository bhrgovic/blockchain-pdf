import unittest
from flask_testing import TestCase
from blueprints.app import app, file_blockchain
from urllib.parse import quote

class TestSearchEndpoint(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_add_pdf(self):
        # Create a JSON object for the PDF
        pdf = {
            "pdf_name": "test_pdf",
            "pdf_data": "test_data"
        }

        # Add the PDF to the blockchain
        file_blockchain.add_pdf(pdf)

        # Search for the PDF
        pdf_data = file_blockchain.search_pdf(pdf["pdf_name"])

        # Check that the PDF data is correct
        self.assertEqual(pdf_data, pdf["pdf_data"])



    def test_search_pdf_found(self):
        # Add a PDF to the blockchain
        pdf = {"pdf_name": "test_pdf", "pdf_data": "test_data"}
        file_blockchain.add_pdf(pdf)

        # Search for the PDF
        response = self.client.get('/search?pdf_name=' + quote(pdf["pdf_name"]))
        print(response.data)  # Print the response data

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the response data is correct
        self.assertEqual(response.json, {"status": "found", "pdf_data": "test_data"})

    def test_search_pdf_not_found(self):
        # Search for a PDF that does not exist
        response = self.client.get('/search?pdf_name=' + quote("non_existent_pdf"))
        print(response.data)  # Print the response data

        # Check that the status code is 404
        self.assertEqual(response.status_code, 400)

        # Check that the response data is correct
        self.assertEqual(response.json, {"status": "not found", "message": "PDF with name 'non_existent_pdf' not found in the blockchain or transaction pool."})
if __name__ == '__main__':
    unittest.main()