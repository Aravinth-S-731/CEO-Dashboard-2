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
