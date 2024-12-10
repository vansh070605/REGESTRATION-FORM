# **Flask Registration Form**

This is a simple Flask web application that provides a user-friendly interface for registration. The entered data is stored in a SQLite database and can be viewed in a tabular format. The project is deployed using **Vercel**.

---

## **Features**
- User Registration Form with validation.
- Stores user data in a persistent SQLite database.
- Displays registered user data in a tabular format.
- Password toggle feature for secure visibility.
- Responsive design for better user experience.
- Persistent data storage for reliability.

---

## **Project Structure**
```
registration-app/
├── api/
│   └── app.py         # Flask backend application
├── templates/
│   ├── index.html     # Registration Form
│   ├── success.html   # Success Page
│   └── display.html   # Table displaying registered users
├── static/
│   └── forms.css      # Styling for the application
├── users.db           # SQLite database to store user data
└── README.md          # Project documentation
```

---

## **Getting Started**

### **Prerequisites**
- Python 3.x installed.
- Basic understanding of Flask and SQLite.
- Node.js installed for deploying with Vercel.

---

### **Installation**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd registration-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python -c "from api.app import init_db; init_db()"
   ```

4. Run the application:
   ```bash
   python api/app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## **Deployment**
This project is configured to deploy on **Vercel**.

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy the project:
   ```bash
   vercel
   ```

3. Access your live project via the Vercel-provided URL.

---

## **Usage**
- Fill out the registration form and click **Submit**.
- View your entered data on the success page.
- Navigate to the **Registered Users** page to see all saved records.

---

## **Technology Stack**
- **Backend**: Flask
- **Frontend**: HTML, CSS
- **Database**: SQLite
- **Deployment**: Vercel

---

## **Contributing**
Feel free to fork the repository and submit a pull request with improvements or new features.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## **Contact**
For any questions or feedback, contact me at: vansh070605@gmail.com
