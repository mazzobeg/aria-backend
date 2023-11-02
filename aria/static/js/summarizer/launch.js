/**
 * 
 * @param {Element} element 
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
 * Create a function to request (ajax) /articles/summarize/status and log results
 */
function fetchAndDisplayStatus() {
    $.ajax({
        url: "/articles/summarize/status",
        type: "GET",
        success: function (data) {
            console.log(data);
            if (data.running == true) {
                document.getElementById('summarize-trigger-spinner').attributes.removeNamedItem('hidden');
                document.getElementById('action-summarize').attributes.setNamedItem(document.createAttribute('disabled'));
            } else if (data.running == false) {
                console.log('Summarization is not running');
                document.getElementById('summarize-trigger-spinner').attributes.setNamedItem(document.createAttribute('hidden'));
                document.getElementById('action-summarize').textContent = 'Summarize';
                document.getElementById('action-summarize').attributes.removeNamedItem('disabled');
            } else {
                throw new Error('Incorrect response from server');
            }
        },
        error: function (error) {
            console.error('Erreur :', error);
        }
    });
}

fetchAndDisplayStatus();
setInterval(fetchAndDisplayStatus, 1000);