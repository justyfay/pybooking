document.addEventListener("DOMContentLoaded", function () {
    let input = document.querySelector('[id=searchLocation]')
    input.addEventListener("keyup", async function (event) {
            let searchData = document.getElementById("searchLocation").value;
            event.preventDefault();

            const listLocations = document.querySelector('[id=list-locations]');
            const locationRequest = new Request("/geo?location=" + searchData);
            if (searchData.length >= 3) {
                fetch(locationRequest)
                    .then((response) => response.json())
                    .then((data) => {
                        for (let i = 0; i < data.length; i++) {
                            const listItem = document.createElement("option");
                            let labelName
                            if (data[i].type === 'city') {
                                labelName = 'Город';
                            } else if (data[i].type === 'region') {
                                labelName = 'Регион';
                            } else if (data[i].type === 'country') {
                                labelName = 'Страна';
                            }
                            listItem.setAttribute('value-type', data[i].type)
                            listItem.setAttribute('label', labelName)
                            let xpath = `//option[text()='${data[i].name}']`;
                            if (!document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue) {
                                listItem.textContent = data[i].name;
                                listLocations.appendChild(listItem);
                            }
                        }
                    })
                    .catch(console.error);
            }
            let opts = document.getElementById('list-locations').children;
            for (let i = 0; i < opts.length; i++) {
                if (opts[i].value === searchData) {
                    document.getElementById("searchLocation").setAttribute('value-type', opts[i].getAttribute('value-type'))
                    document.getElementById("searchLocation").setAttribute('value', opts[i].value)
                    break;
                }
            }
        }
    )
})

async function getCurrentDate() {
    let currentDate = new Date().toJSON().slice(0, 10);
    document.getElementById("startDate").setAttribute('min', currentDate)
    document.getElementById("endDate").setAttribute('min', currentDate)
}

async function searchPage() {
    let location = document.getElementById("searchLocation").value
    let locationType = document.getElementById("searchLocation").getAttribute('value-type')
    let startDate = document.getElementById("startDate").value
    let endDate = document.getElementById("endDate").value
    let url = `/hotels/results?location_name=${location}&location_type=${locationType}&arrival_date=${startDate}&departure_date=${endDate}`
    await fetch(url, {
        method: 'GET',
    }).then(response => {
        if (response.status === 200) {
            window.location.href = `/search?page=1&location_name=${location}&location_type=${locationType}&arrival_date=${startDate}&departure_date=${endDate}`
        }
    });

}
