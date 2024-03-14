// AJAX Helpers
function getCSRFTokenFromMeta() {
    return document.querySelector(
        'meta[name="csrf-token"]'
    ).content;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Mengecek apakah cookie memiliki nama yang sesuai
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function getCSRFToken() {
    const csrfTokenFromCookie = getCookie('csrftoken');
    return csrfTokenFromCookie || getCSRFTokenFromMeta();
}

function getHeaders(type) {
    return {
        "X-CSRFToken": getCSRFToken(),
        'Content-Type': type ?? 'application/json',
    };
}

function checkStatus(status, startNum) {
    return String(status).startsWith(startNum);
}

axios.defaults.headers.common['X-CSRFToken'] = getCSRFToken();
axios.defaults.headers.post['Content-Type'] = 'application/json';

