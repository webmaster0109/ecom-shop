const loadingDiv = document.getElementById('loadingPage');

document.addEventListener('DOMContentLoaded', () => {
    if (loadingDiv) {
        loadingDiv.style.display = 'none';
    }
})

window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        window.location.reload();
    }
})

async function loadingPage(e, productLink) {
    e.preventDefault();
    const ahrefLink = productLink.getAttribute('href');
    console.log(ahrefLink);

    if (ahrefLink) {
        loadingDiv.style.display = 'block';
    }

    setTimeout(() => {
        window.location.href = ahrefLink;
    }, 2000);
}

