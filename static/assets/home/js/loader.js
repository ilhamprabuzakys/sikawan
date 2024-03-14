/*==================
    PAGE LOADER
==================*/

function modifyBodyClass() {
    document.body.classList.remove('pace-done');
    document.body.classList.add('pace-running');
}

function modifyPaceDiv() {
    var paceDiv = document.querySelector('div.pace');
    if (paceDiv) {
        paceDiv.classList.remove('pace-inactive');
        paceDiv.classList.add('pace-active');
        paceDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.75)';
    }
}

function validateEl() {
    return targetElement.getAttribute('href') !== '#' && targetElement.getAttribute('href') !== 'javascript:;' && targetElement.getAttribute('href') !== 'javascript:void(0);' && targetElement.getAttribute('target') !== '_blank';
}

function modifyPageOnReload() {
    modifyBodyClass();
    modifyPaceDiv();
}

document.addEventListener('click', function (event) {
    var targetElement = event.target;

    if (targetElement.tagName === 'A' &&
        (targetElement.getAttribute('href') !== '#' && targetElement.getAttribute('href') !== 'javascript:;') && targetElement.getAttribute('href') !== 'javascript:void(0);' && targetElement.getAttribute('target') !== '_blank'
        && !document.activeElement.getAttribute('download')
        ) {

        modifyBodyClass();
        modifyPaceDiv();
    }
});

document.addEventListener('keydown', function (event) {
    if (
        (event.key === 'Enter' || event.key === ' ') &&
        document.activeElement.tagName === 'A' &&
        (document.activeElement.getAttribute('href') !== '#' && document.activeElement.getAttribute('href') !== 'javascript:;') &&
        !document.activeElement.getAttribute('download')  // Tambahkan kondisi ini
    ) {
        modifyBodyClass();
        modifyPaceDiv();
    }
});


window.addEventListener('beforeunload', function () {
    // modifyPageOnReload();
});