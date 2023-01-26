

function validate () {

    if (validateUsername() && validatePassword()) {
        return true;
    }
    return false
}

function validateUsername () {
    const username = document.getElementById('username').value;

    if (username.length < 5 || username.length > 15) {
        error("Username must consist of 5 to 15 characters.");
        return false
    } else if (!isNaN(username[0]) || !isNaN(username[username.length - 1])) {
        error("No numbers at the beginning or the end");
        return false
    } else if (!/^[A-Za-z0-9]*$/.test(username)) {
        error("Only letters and numbers are allowed")
        return false
    }
    else {
        error('', false)
        return true
    }

}
function validatePassword () {

    const password = document.getElementById('password').value
    const confirmPass = document.getElementById('confirm-password').value

    if (password.length < 8) {
        error("Password must be at least 8 characters");
        return false
    } else if (password !== confirmPass) {
        error("password mismatch")
        return false
    }else {
        error('', false)
        return true
    }
}

function error (message='', show=true) {

    const error = document.querySelector('.error');
    if (show) {
        error.textContent = "*" + message;
    } else {
        error.textContent = "";
    }
}

const submitBtn = document.querySelector('.login_form-btn')
submitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    if (validate()) {
        document.querySelector('.login_form').submit()
    }
})