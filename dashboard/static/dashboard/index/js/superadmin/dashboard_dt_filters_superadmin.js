const keterangan = {
    tahun: $('#filter__tahun').val(),
    tipe: '',
    awal: '',
    akhir: '',
    text: '-',
};

function getSuperAdminURL(tahun, tipe, awal, akhir) {
    let url = `/dashboard/masters/api/v1/provinsi_all_rawan/?format=datatables`;

    let tipe_filter = ``;
    let awal_filter = '';
    let akhir_filter = '';

    if (tipe && tipe != '') {
        tipe_filter += `&${tipe}_${tahun}_range`; // &bahaya_2023_range_min
    }

    if (awal && awal != '') {
        awal_filter += `_min=${awal}`;
        url += tipe_filter + awal_filter;
    }
    
    if (akhir && akhir != '') {
        akhir_filter += `_max=${akhir}`;
        url += tipe_filter +  akhir_filter;
    }

    return url;
}


// Handle keterangan
function generateFiltterKeteranganText() {
    if (!keterangan.tipe) keterangan.tipe = '-';
    keterangan.tipe = capitalizeFirstChar(keterangan.tipe);

    let text = `Mencari data provinsi pada tahun <b>${keterangan.tahun}</b> yang jumlah <b>${keterangan.tipe}</b> nya itu memiliki kriteria`;
    let kriteria = `<li>`;
    
    if (keterangan.akhir && keterangan.akhir != '' && keterangan.akhir != 0) {
        if (keterangan.awal && keterangan.awal != '' && keterangan.awal != 0) {
            kriteria += `Yang dimana jumlah data ${keterangan.tipe} berada diantara batas awal <b>${keterangan.awal}</b> dan <b>${keterangan.akhir}</b> dan kawasan </li>`
        } else {
            kriteria += `Yang dimana maksimal dari jumlah data ${keterangan.tipe} hanya <b>${keterangan.akhir}</b> kawasan </li>`

        }
    }
    
    if (keterangan.awal && keterangan.awal != '' && keterangan.awal != 0) {
        if (keterangan.akhir && keterangan.akhir != '' && keterangan.akhir != 0) {
            kriteria += `Yang dimana jumlah data ${keterangan.tipe} berada diantara batas awal <b>${keterangan.awal}</b> dan <b>${keterangan.akhir}</b> dan kawasan </li>`
        } else {
            kriteria += `Yang dimana minimum dari jumlah data ${keterangan.tipe} hanya <b>${keterangan.awal}</b> kawasan </li>`

        }
    }

    let kriteria_ul = `<ul class="mt-2">${kriteria}</ul>`;

    const result = `${text} ${kriteria_ul}.`;

    keterangan.text = result;

    return result;
}

$('#filter__tahun').on('change', function() {
    keterangan.tahun = $(this).val();

    const result = generateFiltterKeteranganText();

    $('#filter__keterangan').html(result);
});

$('#filter__tipe').on('change', function() {
    keterangan.tipe = $(this).val();

    const result = generateFiltterKeteranganText();

    $('#filter__keterangan').html(result);
});

$('#filter__awal').on('keyup', function() {
    keterangan.awal = $(this).val();

    const result = generateFiltterKeteranganText();

    $('#filter__keterangan').html(result);
});

$('#filter__akhir').on('keyup', function() {
    keterangan.akhir = $(this).val();

    const result = generateFiltterKeteranganText();

    $('#filter__keterangan').html(result);
});

function handleApplyFilter() {
    const form = $('#filter_form');

    const filter_tahun = form.find('#filter__tahun').val();
    const filter_tipe = form.find('#filter__tipe').val();
    const filter_awal = form.find('#filter__awal').val();
    const filter_akhir = form.find('#filter__akhir').val();

    console.log({filter_tahun, filter_tipe, filter_awal, filter_akhir})

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
    form.find('#filter__keterangan').html('');


    const url = getSuperAdminURL('', '', '', '');

    console.log('URL:', url);

    table.ajax.url(url).load();
}