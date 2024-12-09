const today = new Date();
const minAgeDate = new Date(today.setFullYear(today.getFullYear() - 18));
const minDate = minAgeDate.toISOString().split('T')[0];
document.getElementById('dob').setAttribute('min', minDate);
function togglePassword() {
    var passwordField = document.getElementById('password');
    
    if (passwordField.type === "password") {
        passwordField.type = "text";  // Show password
    } else {
        passwordField.type = "password";  // Hide password
    }
}
document.getElementById("exportBtn").addEventListener("click", function () {
    // Get table data
    var table = document.querySelector(".user-table");
    var wb = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });
    
    // Export the data to Excel
    XLSX.writeFile(wb, "UserData.xlsx");
});
