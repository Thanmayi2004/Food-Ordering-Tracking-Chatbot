## Food Ordering-Tracking Website (Chatbot)

# Description
The Food Ordering Tracking Chatbot is a web application that allows users to order food and track their orders through an AI-powered chatbot.
The chatbot is integrated with Dialogflow and is connected to a backend system with an SQL database to store and update order details.

# Features:
- **Chatbot Integration:** A Dialogflow-powered chatbot that assists users in placing food orders.
- **Order Tracking:** Users can track their orders in real-time using an order ID.
- **Database Integration:** The application uses a MySQL database (pandeyji_eatery) to store and update food orders and their tracking status.
- **Web Interface:** A user-friendly frontend built with HTML and CSS that integrates the chatbot
  
## Tools & Technologies Used
# Frontend:
  - **HTML:** To structure the content of the webpage.
  - **CSS:** To style the webpage and create a responsive design.
  - **JavaScript:** To handle dynamic content and interactions on the page.
    
# Backend:
  - **Python:** The backend is developed using Python, with the main logic handled by the main.py script.
  - **FastAPI:** FastAPI is used as the web framework to handle HTTP requests, manage routes, and serve as the backend of the chatbot application.
  - **Dialogflow:** The chatbot is powered by Dialogflow, a Google AI tool for natural language understanding.
  - **MySQL:** The database for storing food orders and their tracking status.

# Other Tools:
  - **ngrok:** Used to expose the local development server to the internet so Dialogflow can access the chatbot hosted on your local machine.
  - **MySQL Workbench:** Used for managing the MySQL database, creating tables, and running queries.

## Installation & Setup
# Prerequisites:
 - **Python:** Make sure Python 3.6+ is installed on your system.
 - **MySQL:** Install MySQL server and create a database named pandeyji_eatery.
 - **Dialogflow Account:** Create an agent on Dialogflow for the chatbot and connect it to your local server using ngrok.
- **ngrok:** Download and set up ngrok to expose your local server to the internet and generate a secure HTTPS URL for Dialogflow.
  
# Required Libraries:
To run this project, you need to install the following Python libraries:
 - **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
 - **uvicorn:** An ASGI server for serving the FastAPI app.
 - **mysql-connector-python:** A Python MySQL client library to connect your Python application to the MySQL database.

## Steps to Run the Project:

Clone the repository to your local machine:
``git clone https://github.com/Thanmayi2004/Food-Ordering-Tracking-Chatbot.git``

