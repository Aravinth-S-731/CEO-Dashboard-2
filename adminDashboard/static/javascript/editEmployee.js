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

// function addEmployeeRow() {
//     const table = document.getElementById('employee-table').getElementsByTagName('tbody')[0];
//     const newRow = table.insertRow();

//     for (let i = 0; i < 6; i++) {
//         const cell = newRow.insertCell(i);
//         cell.contentEditable = "true";
//     }

//     const actionsCell = newRow.insertCell(6);
//     actionsCell.innerHTML = '<button onclick="deleteEmployeeRow(this)"><i class="fa-solid fa-trash"></i></button>';
// }

function addEmployeeRow() {
    const table = document.getElementById('employee-table').getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();

    const empIdCell = newRow.insertCell(0);
    empIdCell.textContent = '';
    empIdCell.setAttribute('contenteditable', 'true');

    for (let i = 1; i < 6; i++) {
        const cell = newRow.insertCell(i);
        cell.contentEditable = "true";
    }

    const actionsCell = newRow.insertCell(6);
    actionsCell.innerHTML = '<button onclick="deleteEmployeeRow(this)">Delete</button>';
}


function deleteEmployeeRow(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

function saveEmployeeData() {
    const rows = document.querySelectorAll('#employee-table tbody tr');
    const updatedData = [];

    rows.forEach(row => {
        const emp_id = row.cells[0].textContent.trim();
        const name = row.cells[1].textContent.trim();
        const age = row.cells[2].textContent.trim();
        // Get the selected value from the <select> element for department
        const department = row.cells[3].querySelector('select').value.trim();
        const salary = row.cells[4].textContent.trim();
        // Get the selected value from the <select> element for gender
        const gender = row.cells[5].querySelector('select').value.trim();

        updatedData.push({ emp_id, name, age, department, salary, gender });
    });

    fetch('/save-employee-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ employees: updatedData }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = 'Data saved successfully!';
        document.getElementById('message').style.color = 'green';
        console.log(data);
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error saving data!';
        document.getElementById('message').style.color = 'red';
        console.error('Error:', error);
    });
}


function deleteEmployee(emp_id) {
    fetch('/delete-employee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ emp_id }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error deleting employee!');
        }
    })
    .catch(error => {
        alert('Error deleting employee!');
        console.error('Error:', error);
    });
}
