const forgotPasswordForm = document.querySelector('#forgotPasswordForm');
const loading = document.querySelector('#spinnerLoading');

forgotPasswordForm.addEventListener('submit', forgotPassword);

const display = document.getElementById('timer');
const timerDiv = document.getElementById('timerDiv');

function startTimer(durationInSeconds) {
    
    let remainingTime = durationInSeconds;

    const resetButton = document.querySelector('.forget-button');
    resetButton.disabled = true;

    const interval = setInterval(() => {
        timerDiv.style.display = "block";
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;

        display.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        if (remainingTime <= 0) {
            clearInterval(interval);
            timerDiv.style.display = "none";
            resetButton.disabled = false;
        }

        remainingTime -= 1;
    }, 1000);
}

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
                startTimer(data.time_left);
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