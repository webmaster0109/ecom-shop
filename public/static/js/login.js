const form = document.querySelector('#loginForm');
form.addEventListener('submit', loginAuthentication);
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
      createToast(result.message, 'Success');
      setTimeout(() => {
        window.location.replace('/');
      }, 2000);
    } else if (response.status === 400) {
      createToast(result.message, 'Warning');
    } else {
      createToast(result.message, 'Error');
    }
  } catch (error) {
    console.error('An error occurred:', error);
    createToast('An unexpected error occurred.', 'Error');
  } finally {
    loading.style.display = 'none';
  }
}
