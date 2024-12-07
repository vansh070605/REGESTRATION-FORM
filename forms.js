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
