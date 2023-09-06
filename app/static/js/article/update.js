document.querySelectorAll('.custom-select').forEach(element => element.addEventListener('change', function () {
    var selectedOption = this.value;
    var id = this.id;
    console.log(this.classList);
    console.log('think', id, selectedOption);
    //updateDatabase(selectedOption);
}));

function updateDatabase(option) {
    // Envoi de la requête AJAX à votre serveur Flask pour mettre à jour la base de données
    // Vous pouvez utiliser la bibliothèque Axios ou Fetch pour effectuer la requête
    // Par exemple, en utilisant Axios :
    axios.post('/update_database', { selectedOption: option })
        .then(function (response) {
            // Gérer la réponse du serveur si nécessaire
        })
        .catch(function (error) {
            // Gérer les erreurs si nécessaire
        });
}