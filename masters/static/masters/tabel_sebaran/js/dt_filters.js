var s = '';

function getURL() {
    let modified_url = `/dashboard/masters/api/v1/provinsi_all_rawan/?format=datatables`;
    if (s != '') {
        s = convertToTitleCaseAndReplaceSpace(s);
        // modified_url += `&nama_kecamatan=${s}`;
        modified_url += `&s=${s}`;
        // modified_url += `&provinsi=${s}`;
        // modified_url += `&kabupaten=${s}`;
    } else {
        modified_url = '/dashboard/masters/api/v1/provinsi_all_rawan/?format=datatables';
    }
    return modified_url;
}

$(function () {
    let timeoutId;

    $('#__table_wrapper input[type="search"]').on('keyup', function () {
        // Menghapus timeout yang ada jika ada
        clearTimeout(timeoutId);

        // Menjadwalkan timeout baru untuk menunggu 1 detik sebelum mengirim permintaan jaringan
        timeoutId = setTimeout(() => {
            let s = $(this).val();
            let url = getURL();

            console.log('URL:', url);

            table.ajax.url(url).load();
        }, 1000);
    });

});

function getSuperAdminURL(tahun, tipe, awal, akhir) {
    let url = `/dashboard/masters/api/v1/provinsi_all_rawan/?format=datatables`;

    let tipe_filter = ``;
    let awal_filter = '';
    let akhir_filter = '';

    if (tipe && tipe != '') {
        tipe_filter += `&${tipe}_${tahun}_range`; // &bahaya_2023_range_min
        // url += `&tipe=${tipe}_${tahun}`;
    }

    if (awal && awal != '') {
        awal_filter += `_min=${awal}`;
        url += tipe_filter + awal_filter;
    }

    if (akhir && akhir != '') {
        akhir_filter += `_max=${akhir}`;
        url += tipe_filter + akhir_filter;
    }

    return url;
}


function handleApplyFilter() {
    const form = $('#filter_form');

    const filter_tahun = form.find('#filter__tahun').val();
    const filter_tipe = form.find('#filter__tipe').val();
    const filter_awal = form.find('#filter__awal').val();
    const filter_akhir = form.find('#filter__akhir').val();

    console.log({
        filter_tahun,
        filter_tipe,
        filter_awal,
        filter_akhir
    })

    const url = getSuperAdminURL(filter_tahun, filter_tipe, filter_awal, filter_akhir);

    console.log('URL:', url);

    table.ajax.url(url).load();
}

function handleResetFilter() {
    const form = $('#filter_form');

    form.find('#filter__tahun').val('').trigger('change');
    form.find('#filter__tipe').val('').trigger('change');
    form.find('#filter__awal').val('').trigger('change');
    form.find('#filter__akhir').val('').trigger('change');


    const url = getSuperAdminURL('', '', '', '');

    console.log('URL:', url);

    table.ajax.url(url).load();
}