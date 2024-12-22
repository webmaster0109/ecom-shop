const forgotPasswordForm = document.querySelector('#forgotPasswordForm');
const message = document.querySelector('#messageId');
const loading = document.querySelector('#spinnerLoading');

forgotPasswordForm.addEventListener('submit', forgotPassword);

async function forgotPassword(e) {
    e.preventDefault();

    const formData = new FormData(forgotPasswordForm);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        loading.style.display = 'inline-block';
        const res = await fetch('/account/forgot-password-attempt/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        });
    
        const data = await res.json();
    
        if (res.ok) {
            message.innerHTML = data.message;
            message.style.color = 'green';
            setTimeout(() => {
                window.location.replace('/account/login/');
            }, 2000);
        } else {
            message.innerHTML = data.message;
            message.style.color = 'red';
        }
        
    } catch (error) {
        console.error('An error occurred:', error);
        message.style.color = 'red';
        message.innerHTML = 'Something went wrong. Please try again later.';        
    } finally {
        loading.style.display = 'none';
        setTimeout(() => {
            message.innerHTML = '';
        }, 3000);
    }
}