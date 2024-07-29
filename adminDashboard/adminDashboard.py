from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
import mysql.connector
from datetime import datetime

adminDashboard = Blueprint('adminDashboard', __name__, template_folder='templates', static_folder='static', static_url_path='/adminDashboard/static')

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Arvi7777",
    database="ceo-revenue"
)


@adminDashboard.route('/view-data', methods=['POST'])
def view_data():
    if 'loggedin' in session and session['role'] == "Admin":
        data = request.json
        selected_month = data.get('selected_month')
        
        if selected_month:
            cursor = mydb.cursor(dictionary=True)

            # Fetch data for the selected month with formatted date
            fetch_query = f"""
            SELECT DATE_FORMAT(date, '%a, %d %b %Y') AS date, revenue, expense, profit
            FROM `{selected_month}`
            """
            cursor.execute(fetch_query)
            month_data = cursor.fetchall()
            cursor.close()

            return jsonify({'month_data': month_data}), 200
        
        return jsonify({'message': 'Selected month not provided'}), 400

    return jsonify({'message': 'Unauthorized'}), 401


@adminDashboard.route('/save-data', methods=['POST'])
def save_data():
    if 'loggedin' in session and session['role'] == "Admin":
        data = request.json

        selected_month = data.get('selected_month')
        if selected_month:
            cursor = mydb.cursor()

            for entry in data['data']:
                # Convert date to YYYY-MM-DD format
                date_obj = datetime.strptime(entry['date'], '%a, %d %b %Y')
                formatted_date = date_obj.strftime('%Y-%m-%d')

                update_query = f"""
                                UPDATE `{selected_month}`
                                SET revenue = %s, expense = %s, profit = %s
                                WHERE date = %s
                                """
                cursor.execute(update_query, (entry['revenue'], entry['expense'], entry['profit'], formatted_date))

            mydb.commit()
            cursor.close()

            return {'message': 'Data saved successfully'}, 200
        else:
            return {'message': 'Selected month not provided'}, 400

    return {'message': 'Unauthorized'}, 401


@adminDashboard.route('/admin', methods=['GET'])
def admin():
    if 'loggedin' in session and session['role'] == "Admin":
        return render_template('selectMonth.html',
                                username = session['username'],
                                email = session['email'],
                                role = session['role'],)

    return redirect(url_for('auth.login'))


@adminDashboard.route('/edit-employee', methods=['GET'])
def edit_employee():
    if 'loggedin' in session and session['role'] == "Admin":
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `ceo-application`.employee_details")
        employees = cursor.fetchall()
        cursor.close()
        return render_template('editEmployee.html',
                                employees=employees,
                                username = session['username'],
                                email = session['email'],
                                role = session['role'],)
    return redirect(url_for('login'))


@adminDashboard.route('/save-employee-data', methods=['POST'])
def save_employee_data():
    if 'loggedin' in session and session['role'] == "Admin":
        data = request.json
        cursor = mydb.cursor()

        for employee in data['employees']:
            print(employee)
            department = employee.get('department', '').strip()
            gender = employee.get('gender', '').strip()
            print(department, gender)

            # Check if emp_id is valid
            if int(employee['emp_id']) > 49:
                # Insert new employee
                insert_query = """
                    INSERT INTO `ceo-application`.employee_details (emp_id, name, age, department, salary, gender)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                try:
                    cursor.execute(insert_query, (employee['emp_id'], employee['name'], employee['age'], department, employee['salary'], gender))
                except mysql.connector.IntegrityError as e:
                    # Handle duplicate emp_id or other integrity errors
                    print(f"Error: {e}")
            else:
                # Update existing employee
                update_query = """
                    UPDATE `ceo-application`.employee_details
                    SET name = %s, age = %s, department = %s, salary = %s, gender = %s
                    WHERE emp_id = %s
                """
                cursor.execute(update_query, (employee['name'], employee['age'], department, employee['salary'], gender, employee['emp_id']))

        mydb.commit()
        cursor.close()
        return {'message': 'Data saved successfully'}, 200

    return {'message': 'Unauthorized'}, 401


@adminDashboard.route('/delete-employee', methods=['POST'])
def delete_employee():
    if 'loggedin' in session and session['role'] == "Admin":
        data = request.json
        emp_id = data.get('emp_id')

        if emp_id:
            cursor = mydb.cursor()
            delete_query = "DELETE FROM `ceo-application`.employee_details WHERE emp_id = %s"
            cursor.execute(delete_query, (emp_id,))
            mydb.commit()
            cursor.close()
            return {'success': True}, 200

        return {'message': 'Employee ID not provided'}, 400

    return {'message': 'Unauthorized'}, 401
