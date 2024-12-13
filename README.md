# **Flask Registration Form**

This is a simple Flask web application that provides a user-friendly interface for user registration. The entered data is stored in a SQLite database and can be viewed in a tabular format. The project is deployed using **Vercel** for seamless accessibility.

---

## **Features**
- **User-Friendly Registration**: Collects user information with input validation.
- **Secure Password Handling**: Toggle visibility feature for passwords.
- **Data Persistence**: Stores data in a reliable SQLite database.
- **View Registered Users**: Displays registered user data in a tabular format.
- **Responsive Design**: Ensures compatibility across devices.
- **Export Feature**: Allows exporting user data as a file.
- **Deployed with Vercel**: Quick and scalable deployment.

---

## **Project Structure**
```
registration-app/
├── api/
│   └── app.py                # Flask backend application
├── templates/
│   ├── index.html            # Registration Form
│   ├── success.html
│   ├── add_family_member.html
│   ├── login.html
│   ├── admin.html
│   └── display.html          # Table displaying registered users
├── static/
│   ├── forms.css             # Styling for the forms
│   ├── success.css           # Styling for the success page
│   ├── admin.css
├── regestration_system.sql   # SQLite database to store user data
└── README.md                 # Project documentation
```

---

## **Getting Started**

### **Prerequisites**
- Python 3.x installed.
- Basic understanding of Flask and SQLite.
- Node.js installed for deployment with Vercel.

---

### **Installation**
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd registration-app
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   ```bash
   python -c "from api.app import init_db; init_db()"
   ```

5. **Run the Application**:
   ```bash
   python api/app.py
   ```

6. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## **Deployment**
This project is configured to deploy on **Vercel** for live hosting.

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy the Project**:
   ```bash
   vercel
   ```

3. **Access Your Live Project**:
   The Vercel CLI will provide a deployment URL for your project.

---

## **Usage**
- Navigate to the **registration form** and fill out the details.
- Submit the form to store the information in the database.
- The **success page** will display a confirmation message.
- Use the **Registered Users** page to view and manage saved records.
- Export user data with the export button on the display page.

---

## **Technology Stack**
- **Backend**: Flask
- **Frontend**: HTML, CSS
- **Database**: SQLite
- **Deployment**: Vercel

---

## **Contributing**
Contributions are welcome! Feel free to fork the repository and submit a pull request with new features, bug fixes, or improvements.

---

## **License**
This project is licensed under the **MIT License**. Refer to the `LICENSE` file for details.

---

## **Contact**
For questions or feedback, feel free to reach out:
- **Email**: vansh070605@gmail.com
