document.addEventListener("DOMContentLoaded", function () {
    let searchParams = new URLSearchParams(window.location.search);

    let location = searchParams.get('location_name');
    let type = searchParams.get('location_type');
    let startDate = searchParams.get('arrival_date');
    let endDate = searchParams.get('departure_date');

    document.querySelector('[id=searchLocation]').value = location;
    document.getElementById("searchLocation").setAttribute('value-type', type);
    document.querySelector('[id=startDate]').value = startDate;
    document.querySelector('[id=endDate]').value = endDate;

    if (location && startDate && endDate != null) {
        document.title = `${location}, ${startDate} - ${endDate}`;
    }
})