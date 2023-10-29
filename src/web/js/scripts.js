document.addEventListener('DOMContentLoaded', async function () {
    const API_URL = window.location.origin + '/api';

    const zoomist = new Zoomist('.zoomist-container', {
        maxScale: 4,
        bounds: true,
        slider: true,
        zoomer: true,
        draggable: true,
        wheelable: true,
        pinchable: true,
    });

    const verticesRequest = await fetch(`${API_URL}/vertices`);
    const vertices = await verticesRequest.json();

    const tripResult = document.getElementById('trip-result');
    const mapResult = document.getElementById('map-result');
    const mapResultContainer = document.getElementById('map-result-container');

    mapResult.addEventListener('load', function () {
        const startVertex = vertices.find((vertex) => vertex.id === parseInt(startInput.getAttribute('data-id')));
        const startX = startVertex.x;
        const startY = startVertex.y;

        zoomist.moveTo(startX, startY);
        //zoomist.zoom(1.5);
    });

    const signTemplate = (line) => {
        const sectionSign = document.createElement('section');
        sectionSign.classList.add('sign');

        const lineName = document.createElement('h1');
        lineName.classList.add('line-name');
        sectionSign.append(lineName);

        const lineType = document.createElement('span');
        lineType.classList.add('line-type');
        lineType.textContent = 'M';
        lineName.append(lineType);

        const lineNameText = document.createElement('span');
        lineNameText.classList.add('sign__line');
        lineNameText.setAttribute('data-line', `m${line}`);
        lineNameText.textContent = line;
        lineName.append(lineNameText);

        const lineStops = document.createElement('ol');
        lineStops.classList.add('line');
        lineStops.setAttribute('data-line', `m${line}`);
        sectionSign.append(lineStops);

        return sectionSign;
    }

    const stationTemplate = (station, correspondances) => {
        const stop = document.createElement('li');
        stop.classList.add('stop');

        const stopName = document.createElement('strong');
        stopName.classList.add('stop__name');
        stopName.textContent = station;
        stop.append(stopName);

        if (correspondances.length > 0) {
            stop.setAttribute('data-transfer', '');
            const stopTransfers = document.createElement('div');
            stopTransfers.classList.add('stop__transfers');

            const mLogo = document.createElement('span');
            mLogo.classList.add('stop__transfer', 'stop__transfer--type-m');
            mLogo.textContent = 'M';

            stopTransfers.append(mLogo);

            correspondances.forEach((correspondance) => {
                const mLine = document.createElement('span');
                mLine.classList.add('stop__transfer', 'stop__transfer--m');
                mLine.setAttribute('data-line', `m${correspondance}`);
                mLine.textContent = correspondance;
                stopTransfers.append(mLine);
            });

            stop.append(stopTransfers);
        }

        return stop;
    }

    const switchTemplate = (oldLine, newLine, duration) => {
        const switchSection = document.createElement('section');
        switchSection.classList.add('switch');

        const switchIcon = document.createElement('img');
        switchIcon.setAttribute('src', 'images/walking.png');
        switchIcon.setAttribute('alt', '');

        const switchTitle = document.createElement('h3');
        switchTitle.textContent = 'Je change de ligne';

        const switchText = document.createElement('p');
        switchText.textContent = `Ligne ${oldLine} à ${newLine}, je suis à ${duration} de trajet.`;

        switchSection.append(switchIcon, switchTitle, switchText);
        return switchSection;
    }

    const arrivalTemplate = (stationName, duration) => {
        const switchSection = document.createElement('section');
        switchSection.classList.add('arrival');

        const switchIcon = document.createElement('img');
        switchIcon.setAttribute('src', 'images/success.png');
        switchIcon.setAttribute('alt', '');

        const switchTitle = document.createElement('h3');
        switchTitle.textContent = 'Bien arrivé !';

        const switchText = document.createElement('p');
        switchText.textContent = `Je suis à la station ${stationName} en ${duration} de trajet.`;

        switchSection.append(switchIcon, switchTitle, switchText);
        return switchSection;
    }

    const autocompleteConfig = {
        autoFirst: true,
        list: vertices,
        data: function (item) {
            return {
                label: `${item.ligne} - ${item.name}`,
                value: item.id,
            };
        },
        replace: function (suggestion) {
            this.input.value = suggestion.label;
            this.input.setAttribute('data-id', suggestion.value);
            this.input.setAttribute('data-name', suggestion.label);

        },
        filter: function (text, input) {
            // be accent insensitive
            text = text.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
            input = input.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace("-", " ");

            return Awesomplete.FILTER_CONTAINS(text, input);
        }
    }

    const startInput = document.getElementById('start');
    const endInput = document.getElementById('end');
    new Awesomplete(startInput, autocompleteConfig);
    new Awesomplete(endInput, autocompleteConfig);

    const tripForm = document.getElementById('trip-form');
    tripForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        mapResult.src = '';

        tripResult.innerHTML = '';
        const startId = startInput.getAttribute('data-id');
        const endId = endInput.getAttribute('data-id');

        if (!startId || !endId) {
            return;
        }

        const bellmanfordRequest = await fetch(`${API_URL}/bellmanford/${startId}/${endId}`);
        const bellmanford = await bellmanfordRequest.json();

        bellmanford.forEach((lineTrip) => {
            const signLine = signTemplate(lineTrip.ligne);
            lineTrip.stations.forEach((station) => {
                signLine.querySelector('.line').append(stationTemplate(station.name, station?.correspondances));
            });


            tripResult.append(signLine);
            if (lineTrip.next_ligne) {
                tripResult.append(switchTemplate(lineTrip.ligne, lineTrip.next_ligne, lineTrip.end_duration_formatted))
            } else {
                tripResult.append(arrivalTemplate(endInput.getAttribute('data-name'), lineTrip.end_duration_formatted))
            }
        });

        // scroll into trip-result
        mapResultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

        mapResult.src = `${API_URL}/bellmanford/map/${startInput.getAttribute('data-id')}/${endInput.getAttribute('data-id')}`;
    });

    const acpmForm = document.getElementById('acpm-form');
    acpmForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        mapResult.src = `${API_URL}/prims/map?duplicated_merge=false`;
    });
});