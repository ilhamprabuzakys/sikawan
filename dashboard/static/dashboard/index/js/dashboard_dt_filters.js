var s = '';

var filter_url = '';

if (role == 'superadmin') {
    filter_url = `/dashboard/masters/api/v1/provinsi_all_rawan/?format=datatables`;
} else if (role == 'bnnp') {
    filter_url = `/dashboard/masters/api/v1/desa/?format=datatables&provinsi=${id_provinsi}`;
} else if (role == 'bnnk') {
    filter_url = `/dashboard/masters/api/v1/desa/?format=datatables&kabupaten=${id_kabupaten}`;
}

function getURL() {
    let modified_url = filter_url;
    if (s != '') {
        s = convertToTitleCaseAndReplaceSpace(s);
        modified_url += `&s=${s}`;
    } else {
        modified_url = filter_url;
    }
    return modified_url;
}

$(function () {
    let timeoutId;

    $('#__table_wrapper input[type="search"]').on('keyup', function () {
        clearTimeout(timeoutId);

        timeoutId = setTimeout(function () {
            s = $(this).val();

            let url = getURL();

            console.log('URL:', url);

            table.ajax.url(url).load();
        }.bind(this), 500);
    });
});