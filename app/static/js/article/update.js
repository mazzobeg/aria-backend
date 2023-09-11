document.querySelectorAll('.custom-select').forEach(element => element.addEventListener('change', function () {
    var selectedOption = this.value;
    var id = this.id;
    console.log(this.classList);
    console.log('think', id, selectedOption);
    //updateDatabase(selectedOption);
}));

function updateDatabase(option) {
    fetch("/")
        .then(function (response) {
            if (response.status === 200) {
                return response.json();
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