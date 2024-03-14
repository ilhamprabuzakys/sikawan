$(function () {
    // Baca parameter dari URL saat halaman dimuat pertama kali
    const urlParams = new URLSearchParams(window.location.search);
    const provinsi = urlParams.get('provinsi');
    const kota = urlParams.get('kabupaten');
    const kecamatan = urlParams.get('kecamatan');
    const param_search = urlParams.get('s');

    if (provinsi || kota || kecamatan || param_search) {
        // Simpan filter dari URL ke dalam variabel selectedValues dan search
        selectedValues.provinsi = provinsi || null;
        selectedValues.kota = kota || null;
        selectedValues.kecamatan = kecamatan || null;
        search = param_search || '';
    
        // Muat data dengan filter dari URL
        table.ajax.url(getDataTableAPIURL()).load();
    }
});

const columns = [{
        data: null,
    },
    // Desa
    {
        data: 'nama_desa',
        render: function (data, type, row) {
            return `<span>${data}</span>`;
        }
    },
    // Kecamatan
    {
        data: 'nama_kecamatan',
        render: function (data, type, row) {
            return `<span>${data}</span>`;
        }
    },
    // Kabupaten
    {
        data: 'nama_kabupaten',
        render: function (data, type, row) {
            return `<span>${data}</span>`;
        }
    },
    // Provinsi
    {
        data: 'nama_provinsi',
        render: function (data, type, row) {
            return `<span>${data}</span>`;
        }
    },
    // Tahun sebelumnya
    {
        data: null,
        render: function (data, type, row) {
            let el = '<div class="text-center">';
            let kawasan_rawan = row.kawasan_rawan[tahun_sebelumnya];

            if (kawasan_rawan) {
                let status = kawasan_rawan.status;
                let id = kawasan_rawan.id;
                let status_class = getStatusClass(status);

                el += `<span class="w-100 rounded-0 btn btn-${status_class}" onclick="handleDetail(${id}, ${tahun_sebelumnya})">${status}</span>`;
            } else {
                el += `<span class="w-100 rounded-0 btn btn-secondary">Kosong</span>`;
            }
            return el += '</div>';
        }
    },
    // Tahun saat ini
    {
        data: null,
        render: function (data, type, row) {
            let el = '<div class="text-center">';
            let kawasan_rawan = row.kawasan_rawan[tahun_saat_ini];

            if (kawasan_rawan) {
                let status = kawasan_rawan.status;
                let id = kawasan_rawan.id;
                let status_class = getStatusClass(status);

                el += `<span class="w-100 rounded-0 btn btn-${status_class}" onclick="handleDetail(${id}, ${tahun_saat_ini})">${status}</span>`;
            } else {
                el += `<span class="w-100 rounded-0 btn btn-secondary">Kosong</span>`;
            }
            return el += '</div>';
        }
    },
    {
        data: null,
        render: function (data, type, row) {
            let detail_button = '';
            let edit_button = '';
            let hapus_button = '';

            let open_container = '<div class="list-button text-uppercase gx-3">';
            let close_container = '</div>';

            let id_desa = row.desa;
            let kawasan_rawan = row.kawasan_rawan[tahun_saat_ini];

            if (kawasan_rawan) {
                let id_kawan = kawasan_rawan.id;
                let nama_desa = row.nama_desa;

                detail_button = `
                <div><a href="javascript:;" class="badge bg-primary text-white text-decoration-none mb-1" onclick="handleDetail(${id_kawan}, '${tahun_saat_ini}')"><i class="fas fa-eye me-2"></i>Lihat detail</a></div>`;

                edit_button = `<div><a href="javascript:void(0)" onclick="handleEdit(${id_kawan}, ${tahun_saat_ini})" class="badge bg-success text-white text-decoration-none mb-1">
                <i class="fas fa-pen-to-square me-2"></i>Edit</a></div>`;

                hapus_button = `<div><a href="javascript:;" onclick="handleDelete(${id_kawan}, '${nama_desa}', ${tahun_saat_ini})" class="badge bg-danger text-white text-decoration-none mb-1"><i class="fas fa-trash-alt me-2"></i>Hapus</a></div>`;
            } else {
                detail_button = `<div><a href="javascript:;" class="badge bg-secondary text-white text-decoration-none mb-1"><i class="fas fa-eye me-2"></i>Lihat detail</a></div>`;

                edit_button = `<div><a href="javascript:void(0)" onclick="handleEdit(${id_desa}, ${tahun_saat_ini}, 'desa')" class="badge bg-success text-white text-decoration-none mb-1"><i class="fas fa-pen-to-square me-2"></i>Edit</a></div>`;

                hapus_button = `<div><a href="javascript:;" class="badge bg-secondary text-white text-decoration-none mb-1"><i class="fas fa-trash-alt me-2"></i>Hapus</a></div>`;
            }

            const list_of_button = open_container + detail_button + edit_button + hapus_button + close_container;

            return list_of_button;
        }
    }

];

var table = $('#__table').DataTable({
    language: dt_lang_config(),
    serverSide: true,
    responsive: true,
    pageLength: 10,
    ajax: {
        url: `/dashboard/masters/api/v1/desa/?format=datatables`,
        dataSrc: 'data'
    },
    ordering: true,
    columns: columns,
    initComplete: function (settings, json) {
        console.log('Hasil fetch data : ', json);
    },
    columnDefs: [dt_row_pagination()]
});