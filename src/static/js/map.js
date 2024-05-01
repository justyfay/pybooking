ymaps.ready(init);

function init() {
    const params = urlParams()

    let myMap = new ymaps.Map('map', {
            center: [55.76, 37.64],
            zoom: 9,
            controls: [],
        }),

        objectManager = new ymaps.ObjectManager();

    ymaps.geocode(params.location, {
        results: 1
    }).then(function (res) {
        let firstGeoObject = res.geoObjects.get(0),
            coords = firstGeoObject.geometry.getCoordinates(),
            bounds = firstGeoObject.properties.get('boundedBy');

        myMap.setBounds(bounds, {
            checkZoomRange: true
        });


        myMap.geoObjects.add(objectManager);

        let mapUrl = new URL(`${window.location.protocol}${window.location.host}/geo/map?page=${params.page}&location_name=${params.location}&location_type=${params.type}&arrival_date=${params.startDate}&departure_date=${params.endDate}`)
        if (params.stars != null) {
            mapUrl.searchParams.append('stars', params.stars)
        }

        $.ajax({
            url: mapUrl.toString()
        }).done(function (data) {
            objectManager.add(data);
        });
        myMap.controls.add('zoomControl');
    })
}
