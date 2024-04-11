document.addEventListener('DOMContentLoaded', function () {
    const params = urlParams()

    document.querySelector('[id=searchLocation]').value = params.location;
    document.getElementById('searchLocation').setAttribute('value-type', params.type);
    document.querySelector('[id=startDate]').value = params.startDate;
    document.querySelector('[id=endDate]').value = params.endDate;

    if (params.location && params.startDate && params.endDate != null) {
        document.title = `${params.location}, ${params.startDate} - ${params.endDate}`;
    }
    const url = new URLSearchParams(window.location.search);
    let checkboxes = document.getElementsByClassName('form-check-input')

    if (params.stars !== null) {
        let paramsArray = params.stars.split(' ')
        for (let y = 0; y < paramsArray.length; y++) {
            try {
                document.querySelector(`input[value="${paramsArray[y]}"]`).setAttribute('checked', 'true')

            } catch (TypeError) {

            }

        }
    }

    try {
        if (params.stars.trim() === '') {
            url.delete('stars')
            url.set('page', "1")
            window.location.search = url.toString()
        }
    } catch (TypeError) {

    }
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].addEventListener('click', function () {
            let checkboxValue = checkboxes[i].getAttribute('value')
            let actualParams = urlParams()
            if (checkboxes[i].getAttribute('checked') === null) {
                url.set('stars', checkboxValue);
                url.set('page', "1");
            }
            if (params.stars !== null && params.stars.indexOf(checkboxValue) === -1) {
                let newVal = checkboxValue + ' ' + params.stars
                url.set('stars', newVal)
                url.set('page', "1");
            }
            if (checkboxes[i].getAttribute('checked') !== null) {
                checkboxes[i].removeAttribute('checked')
                let newVal = actualParams.stars.replace(checkboxValue, "")
                url.set('stars', newVal)
                url.set('page', "1");
            }
            window.location.search = url.toString()
        });
    }

})

function urlParams() {
    let searchParams = new URLSearchParams(window.location.search);

    let location = searchParams.get('location_name');
    let type = searchParams.get('location_type');
    let startDate = searchParams.get('arrival_date');
    let endDate = searchParams.get('departure_date');
    let stars = searchParams.get('stars');
    return {location, type, startDate, endDate, stars}
}

function urlBuilder(currentPage) {
    const params = urlParams()
    let url = `/search?page=${currentPage}&location_name=${params.location}&location_type=${params.type}&arrival_date=${params.startDate}&departure_date=${params.endDate}`
    if (params.stars != null) {
        url = url + `&stars=${params.stars}`
    }
    return url
}

function previousButton(currentPage, paginationList) {
    let previousLink = document.createElement('a')
    previousLink.className = 'page-link'
    let previousItem = document.createElement('li')

    if (currentPage - 1 !== 0) {
        previousLink.setAttribute(
            'href',
            urlBuilder(Number(currentPage) - 1)
        )
    } else {
        previousItem.className = 'disabled'
    }

    previousLink.innerText = 'Назад'
    previousItem.appendChild(previousLink)
    paginationList.appendChild(previousItem)
}

function forwardButton(currentPage, paginationList, totalPages) {
    let forwardLink = document.createElement('a')
    forwardLink.className = 'page-link'
    let forwardItem = document.createElement('li')
    if (currentPage !== totalPages) {
        forwardLink.setAttribute(
            'href',
            urlBuilder(Number(currentPage) + 1)
        )
    } else {
        forwardItem.className = 'disabled'
    }
    forwardLink.innerText = 'Вперед'
    forwardItem.appendChild(forwardLink)
    paginationList.appendChild(forwardItem)
}

function previousSlice(paginationList) {
    try {
        let previousSlice = paginationList.children[2];
        let previousSliceLink = previousSlice.getElementsByTagName('a')[0]
        let previousSlicePage = Number(paginationList.children[3].innerText) - 1

        if (previousSlice.innerText === '...') {
            previousSliceLink.setAttribute('href', urlBuilder(previousSlicePage))
        }
    } catch (TypeError) {
    }
}

function nextSlice(paginationList) {
    try {
        let nextSlice = paginationList.children[paginationList.children.length - 2];
        let nextSliceLink = nextSlice.getElementsByTagName('a')[0]
        let nextSlicePage = Number(paginationList.children[paginationList.children.length - 3].innerText) + 1
        if (nextSlice.innerText === '...') {
            nextSliceLink.setAttribute('href', urlBuilder(nextSlicePage))
        }
    } catch (TypeError) {
    }
}

function pagination(totalPages) {
    const allPages = []

    for (let i = 1; i <= totalPages; i++) {
        allPages.push(i)
    }
    const sliceSize = 6;
    const slicedPages = [];

    for (let i = 0; i < allPages.length; i += sliceSize) {
        slicedPages.push(allPages.slice(i, i + sliceSize));
    }
    for (let i = 0; i < slicedPages.length; i++) {
        let currentSlice = slicedPages[i]
        if (currentSlice[0] > sliceSize) {
            currentSlice.unshift(1, '...');
        }
        if (currentSlice[currentSlice.length - 1] !== totalPages && (currentSlice[currentSlice.length - 1] < totalPages)) {
            currentSlice.push('...')
            currentSlice.push(Number(totalPages))
        }
    }
    return slicedPages
}

function buildPagination(totalPages, currentPage) {
    let pagesList = pagination(totalPages)
    const paginationList = document.getElementById('paginationList')

    previousButton(currentPage, paginationList)

    let pagesIndex = 0
    let pages = pagesList
    for (let i = 0; i < pages[pagesIndex].length; i++) {

        if (Number(currentPage) > pages[pagesIndex][pages[pagesIndex].length - 3]
            && pages[pagesIndex][pages[pagesIndex].length - 2] === '...') {
            pagesIndex += 1
        }
        let linkItem = document.createElement('a')
        linkItem.className = 'page-link page-num'
        linkItem.setAttribute(
            'href',
            urlBuilder(pages[pagesIndex][i])
        )
        linkItem.innerText = pages[pagesIndex][i]


        let paginationItem = document.createElement('li')

        if (pages[pagesIndex][i] === Number(currentPage)) {
            paginationItem.className = 'page-item page-number active'
        } else {
            paginationItem.className = 'page-item page-number'
        }
        paginationItem.appendChild(linkItem)
        paginationList.appendChild(paginationItem)


    }

    previousSlice(paginationList)
    nextSlice(paginationList)

    forwardButton(currentPage, paginationList, totalPages)
}
