Installation and Setup

Prerequisites
Python 3.8 or higher
MongoDB installed and running on localhost


Setting up the Web Service

Install the required dependencies:
pip install -r requirements.txt

The JSON files for the 3 collections are available, one has to import these JSON files into a database named "book_shopping"

Start the FastAPI server in main.py file:
uvicorn main:app --reload

Client application:R
Run the command
python client.py

Observe the output in the terminal, which should show the sequence of actions performed by the client (querying a product and placing an order).
