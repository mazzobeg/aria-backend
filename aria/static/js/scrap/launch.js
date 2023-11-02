/**
 * 
 * @param {Element} element 
 */
async function triggerScrapers(element) {
    element.setAttribute('disabled', 'true')
    fetch('/trigger_scraping')
        .then(function (response) {
            if (response.status === 200) {
                element.removeAttribute('disabled')
            } else {
                throw new Error('Échec de la requête');
            }
        })
        .then(function (data) {
            console.log(data);
        })
        .catch(function (error) {
            console.error('Erreur :', error);
        });
}

function fetchAndDisplayState() {
    let element = document.getElementById('action-scraper');
    fetch('/control/scraper/state')
        .then(response => {
            if (!response.ok) {
                throw new Error('La requête a échoué.');
            }
            return response.json();
        })
        .then(data => {
            // Affichez la propriété 'state' dans la div 'result'
            if (data.state) {
                element.setAttribute('disabled', 'true')
            } else {
                element.removeAttribute('disabled')
            }
        })
        .catch(error => {
            console.error('Erreur :', error);
            document.getElementById('result').textContent = 'Erreur lors de la récupération de l\'état.';
        });
}

// Appelez fetchAndDisplayState toutes les 5 secondes
setInterval(fetchAndDisplayState, 5000);

// Appelez fetchAndDisplayState immédiatement pour la première fois
fetchAndDisplayState();