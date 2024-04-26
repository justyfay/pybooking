document.addEventListener("DOMContentLoaded", function () {
    let input = document.querySelector('[id=searchLocation]')
    input.addEventListener("keyup", async function (event) {
            let searchData = document.getElementById("searchLocation").value;
            event.preventDefault();
            if (searchData.length >= 3) {
                $(function () {
                    const locationRequest = `/geo?location=${searchData}`
                    $.getJSON(locationRequest, function (src) {
                        let data = src.map(function (v) {
                            return {
                                value: v.name,
                                type: v.type
                            };
                        });
                        $("#searchLocation").autocomplete({
                            source: data,
                            select: function (event, ui) {
                                $("#searchLocation").text(ui.item.value)
                                document.getElementById("searchLocation").setAttribute('value-type', ui.item.type)
                                document.getElementById("searchLocation").setAttribute('value', ui.item.value)
                            },
                        });
                    });
                });
            }
            $.widget("custom.autocomplete", $.ui.autocomplete, {
                _renderItem: function (ul, data) {
                    let labelName
                            if (data.type === 'city') {
                                labelName = 'Город';
                            } else if (data.type === 'region') {
                                labelName = 'Регион';
                            } else if (data.type === 'country') {
                                labelName = 'Страна';
                            }
                    let li = $('<li>').attr('value-type', data.type);
                    li.attr('value', data.value).appendTo(ul);
                    let div = $('<div>').appendTo(li)
                    let locationNameSpan = $('<span class="locationName">')
                    let locationTypeSpan = $('<span class="locationPosition">')
                    locationNameSpan.append(data.value).appendTo(div)
                    locationTypeSpan.append(labelName).appendTo(div)
                    return li;
                }
            });
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
