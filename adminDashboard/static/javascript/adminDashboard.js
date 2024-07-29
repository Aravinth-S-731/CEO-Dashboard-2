let navLinks = document.getElementById("navLinks");
const transactionHistoryDiv = document.getElementById("transaction-history");

function openDashboardNav(){
    navLinks.style.left = "0";
}
function closeDashboardNav(){
    navLinks.style.left = "-200px";
}

const navListLinks = document.querySelectorAll('ul li');

console.log(role)
if (role === "Admin") {
    adminEditLink.style.display = 'block';
}

function viewData() {
    const selectedMonth = document.getElementById('selected_month').value;
    if (!selectedMonth) {
        alert('Please select a month');
        return;
    }

    fetch('/view-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selected_month: selectedMonth }),
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = ''; // Clear previous data
        data.month_data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.date}</td>
                <td contenteditable="true" data-field="revenue">${row.revenue}</td>
                <td contenteditable="true" data-field="expense">${row.expense}</td>
                <td contenteditable="true" data-field="profit">${row.profit}</td>
            `;
            tableBody.appendChild(tr);
        });
        document.getElementById('month-name').textContent = selectedMonth.charAt(0).toUpperCase() + selectedMonth.slice(1);
        document.getElementById('data-table').style.display = 'block';

        // Add input restriction to the newly created contenteditable elements
        addInputRestrictions();
    })
    .catch(error => {
        alert('Error fetching data!');
        console.error('Error:', error);
    });
}

function saveData() {
    const rows = document.querySelectorAll('tbody tr');
    const updatedData = [];
    const selectedMonth = document.getElementById('selected_month').value;

    rows.forEach(row => {
        const date = row.cells[0].textContent.trim();
        const revenue = row.cells[1].textContent.trim();
        const expense = row.cells[2].textContent.trim();
        const profit = row.cells[3].textContent.trim();
        updatedData.push({ date, revenue, expense, profit });
    });

    fetch('/save-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: updatedData, selected_month: selectedMonth }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = 'Data saved successfully!';
        document.getElementById('message').style.color = 'green';
        console.log(data);
        alert('Data saved successfully!');
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error saving data!';
        document.getElementById('message').style.color = 'red';
        console.error('Error:', error);
    });
}

// Restrict contenteditable cells to numeric input only
function addInputRestrictions() {
    const editableCells = document.querySelectorAll('td[contenteditable="true"]');

    editableCells.forEach(cell => {
        cell.addEventListener('input', function(event) {
            // Allow only digits, decimals, and hyphens (for negative values)
            const regex = /^[0-9]*\.?[0-9]*$/;
            const value = event.target.textContent;

            if (!regex.test(value)) {
                // Remove non-numeric characters
                event.target.textContent = value.replace(/[^0-9.]/g, '');
            }
        });
    });
}

// Initialize input restrictions when the page loads
document.addEventListener('DOMContentLoaded', addInputRestrictions);
