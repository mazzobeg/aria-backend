// create a function requesting (with fetch) at each second /scrapers/status/<scraper_name> with <scraper_name> as parameter and log the status in the console
function fetchAndDisplayState() {
    // get all 'div' elements with class 'card-header' 'scraper-name'
    const scraperNames = document.querySelectorAll('div.card-header.scraper-name');
    scraperNames.forEach(sn => {
        const scraperName = sn.textContent.trim();
        fetch(`/scrapers/status/${scraperName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('La requête a échoué.');
            }
            return response.json();
        })
        .then(data => {
            // add 'disabled' class to tag with id {{scraper.name}}-stop-btn if scraper is not running
            if (data.is_running === false) {
                document.getElementById(`${scraperName}-stop-btn`).classList.add('disabled');
                document.getElementById(`${scraperName}-start-btn`).classList.remove('disabled');
            } else {
                document.getElementById(`${scraperName}-stop-btn`).classList.remove('disabled');
                document.getElementById(`${scraperName}-start-btn`).classList.add('disabled');
            }
        })
        .catch(error => {
            console.error('Erreur :', error);
        });
    })   
}

fetchAndDisplayState();
setInterval(fetchAndDisplayState, 1000);