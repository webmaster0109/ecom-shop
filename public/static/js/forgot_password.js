const forgotPasswordForm = document.querySelector('#forgotPasswordForm');
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
            createToast(data.message, 'Success');
            setTimeout(() => {
                window.location.replace('/account/login/');
            }, 2000);
        } else {
            if (res.status === 400) {
                createToast(data.message, 'Warning');
            } else {
                createToast(data.message, 'Error');
            }
        }
        
        
    } catch (error) {
        console.error('An error occurred:', error);
        createToast('An unexpected error occurred.', 'Error');      
    } finally {
        loading.style.display = 'none';
    }
}