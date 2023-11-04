/**
 * This function triggers the summarization process.
 * It sends a fetch request to the '/articles/summarize/start' endpoint.
 * If the element has a 'disabled' class, the function returns immediately.
 * @param {Element} element - The element to check for the 'disabled' class.
 */
async function triggerSummarization(element) {
    if (element.classList.contains('disabled')) {
        return;
    }
    fetch('/articles/summarize/start')
        .then(function (response) {
            if (response.status === 200) {
                console.log("succees");
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

/**
 * This function sends a GET request to the '/articles/summarize/status' endpoint.
 * It updates the summarization button's CSS based on the response.
 * If the response indicates that the summarization process is running, it sets the button to the 'ON' state.
 * If the response indicates that the summarization process is not running, it sets the button to the 'OFF' state.
 */
function fetchAndDisplayStatus() {
    $.ajax({
        url: "/articles/summarize/status",
        type: "GET",
        success: function (data) {
            if (data.running == true) {
                switchSummarizeBtnCss(SummarizationStatus.ON)
            } else if (data.running == false) {
                switchSummarizeBtnCss(SummarizationStatus.OFF)
            } else {
                throw new Error('Incorrect response from server');
            }
        },
        error: function (error) {
            console.error('Erreur :', error);
        }
    });
}

/**
 * This is an enumeration for the summarization status.
 * It has two possible values: 'ON' and 'OFF'.
 */
const SummarizationStatus = Object.freeze({
    ON: Symbol("on"),
    OFF: Symbol("off")
});

/**
 * This function updates the summarization button's CSS based on the provided status.
 * If the status is 'OFF', it enables the button and hides the spinner.
 * If the status is 'ON', it disables the button and shows the spinner.
 * @param {HTMLElement} element - The summarization button element.
 * @param {SummarizationStatus} summarizationStatus - The status to set the button to.
 */
function switchSummarizeBtnCss(summarizationStatus) {
    let btn = document.getElementById('action-summarize');
    let spinner = document.getElementById('action-summarize-spinner');
    let text = document.getElementById('action-summarize-text');
    if (summarizationStatus == SummarizationStatus.OFF) {
        if (btn.attributes.getNamedItem('disabled') != null)
            btn.attributes.removeNamedItem('disabled');
        if (spinner.attributes.getNamedItem('hidden') == null)
            spinner.attributes.setNamedItem(document.createAttribute('hidden'));
        text.textContent = 'Summarize';
    } else {
        if (btn.attributes.getNamedItem('disabled') == null)
            btn.attributes.setNamedItem(document.createAttribute('disabled'));
        if (spinner.attributes.getNamedItem('hidden') != null)
            spinner.attributes.removeNamedItem('hidden');
        text.textContent = 'Summarizing...';
    }
}

fetchAndDisplayStatus();
setInterval(fetchAndDisplayStatus, 1000);