document.addEventListener("DOMContentLoaded", function () {
    let cards = document.getElementsByClassName('card-link');
    let currentDate = new Date().toJSON().slice(0, 10);
    for (let i = 0; i < 6; i++) {
        console.log(cards[i])
        let cardName = cards[i].textContent;
        console.log(cardName)
        cards[i].setAttribute('href', `/search?location_name=${cardName}&location_type=country&arrival_date=${currentDate}&departure_date=${currentDate}`)
    }
})