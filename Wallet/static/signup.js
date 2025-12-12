const form = document.getElementById('signupForm');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm-password');
const strengthBar = document.getElementById('strengthBar');
const passwordStrength = document.getElementById('passwordStrength');

// Password strength indicator
password.addEventListener('input', function () {
  const value = this.value;
  passwordStrength.style.display = value ? 'block' : 'none';

  let strength = 0;
  if (value.length >= 6) strength++;
  if (value.length >= 10) strength++;
  if (/[A-Z]/.test(value) && /[a-z]/.test(value)) strength++;
  if (/[0-9]/.test(value)) strength++;
  if (/[^A-Za-z0-9]/.test(value)) strength++;

  strengthBar.className = 'password-strength-bar';
  if (strength <= 2) {
    strengthBar.classList.add('strength-weak');
  } else if (strength <= 4) {
    strengthBar.classList.add('strength-medium');
  } else {
    strengthBar.classList.add('strength-strong');
  }
});

// Form validation
form.addEventListener('submit', function (e) {
  e.preventDefault();
  let isValid = true;

  // Reset errors
  document
    .querySelectorAll('.error-message')
    .forEach((el) => (el.style.display = 'none'));

  // Validate password
  if (password.value.length < 6) {
    document.getElementById('passwordError').style.display = 'block';
    isValid = false;
  }

  // Validate confirm password
  if (password.value !== confirmPassword.value) {
    document.getElementById('confirmError').style.display = 'block';
    isValid = false;
  }

  // Validate username
  if (document.getElementById('username').value.length < 3) {
    document.getElementById('usernameError').style.display = 'block';
    isValid = false;
  }

  if (isValid) {
    form.submit();
  }
});
