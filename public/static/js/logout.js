const logout = document.getElementById('userLogout');
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
            createToast('Logging out...', 'Warning');
            setTimeout(() => {
                window.location.replace('/account/login/');
            }, 2000);
        } else {
            createToast('Failed to logout. Please try again later.', 'Error');
        }
    } catch (error) {
        console.error('An error occurred:', error);
        createToast('An unexpected error occurred.', 'Error');
    }
}