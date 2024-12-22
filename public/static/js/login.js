const form = document.querySelector('#loginForm');
form.addEventListener('submit', loginAuthentication);
const message = document.querySelector('#messageId');
const loading = document.querySelector('#spinnerLoading');

async function loginAuthentication(e) {
  e.preventDefault();

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const formData = new FormData(form);

  try {
    loading.style.display = 'inline-block';
    const response = await fetch('/account/login-attempt/', {
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
    message.style.color = 'red';
    message.innerHTML = 'Something went wrong. Please try again later.';
  } finally {
    loading.style.display = 'none';
    setTimeout(() => {
        message.innerHTML = '';
    }, 2000);
}
}