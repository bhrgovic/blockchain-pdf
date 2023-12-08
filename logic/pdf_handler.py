import base64
import PyPDF2

class PdfHandler:    

    def add_pdf_to_blockchain(self, pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            if pdf_reader.getNumPages() > 2:
                print("PDF is too long. Only 1-2 pages are allowed.")
                return

        f.seek(0)  # Seek to the start of the file
        pdf_data = f.read()

        pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")

        new_block = {
            'index': len(self.chain) + 1,
            'pdf_base64': pdf_base64
            # Add other block data like timestamp, previous hash, etc.
        }

        self.chain.append(new_block)

    def read_pdf_from_blockchain(self, index):
        block = self.chain[index]
        pdf_base64 = block.get("pdf_base64")
        if not pdf_base64:
            print("No PDF found in this block.")
            return

        pdf_data = base64.b64decode(pdf_base64)
        pdf_path = f"block_{index}_pdf.pdf"

        with open(pdf_path, "wb") as f:
            f.write(pdf_data)

        print(f"PDF extracted to {pdf_path}")
