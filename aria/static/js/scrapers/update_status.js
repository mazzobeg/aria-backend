
function fetchAndDisplayState() {
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
            if (data.is_running === false) {
                switchScraperBtnCss(ScrapperStatus.OFF, scraperName)
            } else {
                switchScraperBtnCss(ScrapperStatus.ON, scraperName)
            }
        })
        .catch(error => {
            console.error('Erreur :', error);
        });
    })   
}

/**
* This is an enumeration for the summarization status.
* It has two possible values: 'ON' and 'OFF'.
*/
const ScrapperStatus = Object.freeze({
    ON: Symbol("on"),
    OFF: Symbol("off")
});

/**
 * This function updates the summarization button's CSS based on the provided status.
 * If the status is 'OFF', it enables the button and hides the spinner.
 * If the status is 'ON', it disables the button and shows the spinner.
 * @param {HTMLElement} element - The summarization button element.
 * @param {ScrapperStatus} scrapperStatus - The status to set the button to.
 */
function switchScraperBtnCss(scrapperStatus, scraperName) {
    let stopBtn = document.getElementById(`${scraperName}-stop-btn`)
    let startBtn = document.getElementById(`${scraperName}-start-btn`)
    if (scrapperStatus == ScrapperStatus.ON) {
        stopBtn.classList.contains('disabled') ? stopBtn.classList.remove('disabled') : null;
        !startBtn.classList.contains('disabled') ? startBtn.classList.add('disabled') : null;
    } else {
        !stopBtn.classList.contains('disabled') ? stopBtn.classList.add('disabled') : null;
        startBtn.classList.contains('disabled') ? startBtn.classList.remove('disabled') : null;
    }
}

fetchAndDisplayState();
setInterval(fetchAndDisplayState, 1000);