function getAdminURLFilter(kabupaten, kecamatan, status, tahun) {
    let url = `/dashboard/masters/api/v1/desa/?format=datatables&provinsi=${id_provinsi}`;

    if (tahun && tahun != '') {
        selected_tahun = tahun;
    }

    if (status && status != '') {
        url += `&status=${status}_${tahun}`;
    }

    if (kabupaten && kabupaten != '') {
        url += `&kabupaten=${kabupaten}`;
    } else {
        $('#filter__kecamatan').empty();
        $('#filter__kecamatan').append($('<option>', {
            value: '',
            text: '--Pilih kecamatan--',
        }));
        $('#filter__kecamatan').prop('disabled', true);
    }

    if (kecamatan && kecamatan != '') {
        url += `&kecamatan=${kecamatan}`;
    }

    if (s && s != '') {
        s = convertToTitleCaseAndReplaceSpace(s);
        url += `&s=${s}`;
    }

    return url;
}

async function loadFilterKecamatan(kotaId) {
    const kecamatanDropdown = $('#filter__kecamatan');

    if (!kotaId) return;

    kecamatanDropdown.empty();
    kecamatanDropdown.append($('<option>', {
        value: '',
        text: '--Pilih kecamatan--',
    }));

    try {
        const response = await axios.get(`/dashboard/masters/api/v1/list_districts/?kabupaten=${kotaId}`);

        response.data.forEach(kecamatan => {
            kecamatanDropdown.append($('<option>', {
                value: kecamatan.id,
                text: kecamatan.nama_kecamatan
            }));
        });

        kecamatanDropdown.removeAttr('disabled');
    } catch (error) {
        console.error('Error:', error);
    }
}

$('#filter__kabupaten').on('change', async function () {
    $('#filter__kecamatan').val('');

    const selected_kabupaten = $(this).val();

    if (selected_kabupaten != '') {
        await loadFilterKecamatan(selected_kabupaten);
    }
});


function handleApplyFilter() {
    const form = $('#filter_form');

    const filter_kabupaten = form.find('#filter__kabupaten').val();
    const filter_kecamatan = form.find('#filter__kecamatan').val();
    const filter_status = form.find('#filter__status').val();
    const filter_tahun = form.find('#filter__tahun').val();

    const url = getAdminURLFilter(filter_kabupaten, filter_kecamatan, filter_status, filter_tahun);

    console.log('URL:', url);

    table.ajax.url(url).load();
}

function handleResetFilter() {
    const form = $('#filter_form');

    form.find('#filter__kabupaten').val('').trigger('change');
    form.find('#filter__kecamatan').val('').trigger('change');
    form.find('#filter__status').val('').trigger('change');
    form.find('#filter__tahun').val('2023').trigger('change');


    const url = getAdminURLFilter('', '', '', '2023');

    console.log('URL:', url);

    table.ajax.url(url).load();
}