const logout = document.getElementById('userLogout');
const logoutMessage = document.querySelector('#userMessageId');

logout.addEventListener('click', logoutUser);

async function logoutUser(e) {
    e.preventDefault();
    try {
        const response = await fetch('/account/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
        });
    
        if (response.ok) {
            logoutMessage.innerHTML = 'You are logging out...';
            logoutMessage.style.color = 'red';
            setTimeout(() => {
                window.location.replace('/account/login/');
            }, 2000);
        } else {
            console.error('An error occurred:');
            logoutMessage.innerHTML = 'Failed to logout. Please try again later.';
            logoutMessage.style.color = 'red';
        }
    } catch (error) {
        console.error('An error occurred:', error);
        logoutMessage.innerHTML = 'An unexpected error occurred. Please try again later.';
        logoutMessage.style.color = 'red';
    }
}