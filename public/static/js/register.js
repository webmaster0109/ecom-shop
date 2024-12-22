const registerForm = document.getElementById('registerForm');
registerForm.addEventListener('submit', registerUser);
const message = document.getElementById('messageId');
const loading = document.getElementById('spinnerLoading');

async function registerUser(e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(registerForm);

    try {
        loading.style.display = 'inline-block';
        const response = await fetch('/account/register-attempt/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            message.innerHTML = result.message;
            message.style.color = 'green';
            setTimeout(() => {
                window.location.replace('/');
            }, 2000);
        } else {
            message.innerHTML = result.message;
            message.style.color = 'red';
        }
    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        loading.style.display = 'none';
        setTimeout(() => {
            message.innerHTML = '';
        }, 2000);
    }
}