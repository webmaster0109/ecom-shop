document.addEventListener('DOMContentLoaded', () => {
    fetch('/auth/status/')
    .then(response => response.json())
    .then(data => {
        if (data.is_authenticated) {
            if (!localStorage.getItem('reloaded')) {
                localStorage.setItem('reloaded', 'true');
                window.location.replace('/');
            }
        } else {
            localStorage.removeItem('reloaded')
        }
    })
    .catch(error => {
        console.log(error);
    })
})