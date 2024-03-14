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
    {
        data: null,
        render: function (data, type, row) {
            let el = '<div class="text-center">';
            let kawasan_rawan = row.kawasan_rawan[selected_tahun];

            if (kawasan_rawan) {
                let status = kawasan_rawan.status;
                let id = kawasan_rawan.id;
                let status_class = getStatusClass(status);

                el += `<span class="w-100 rounded-0 btn btn-${status_class}" onclick="handleDetail(${id}, ${selected_tahun})">${status}</span>`;
            } else {
                el += `<span class="w-100 rounded-0 btn btn-secondary">Kosong</span>`;
            }
            return el += '</div>';
        }
    },
    {
        data: null,
        render: function (data, type, row) {
            return `<div class="text-center">${selected_tahun}</div>`;
        }
    },
    {
        data: null,
        render: function (data, type, row) {
            let kawasan_rawan = row.kawasan_rawan[selected_tahun];
            let keterangan = '-';
            
            if (kawasan_rawan) keterangan = kawasan_rawan.keterangan

            let el = `${keterangan}`
            return el;
        }
    }
];

var table = $('#__table').DataTable({
    language: dt_lang_config(),
    serverSide: true,
    responsive: true,
    pageLength: 10,
    ajax: {
        url: `/dashboard/masters/api/v1/desa/?format=datatables&kabupaten=${id_kabupaten}`,
        dataSrc: 'data'
    },
    ordering: true,
    columns: columns,
    initComplete: function (settings, json) {
        console.log('Hasil fetch data : ', json);
    },
    columnDefs: [dt_row_pagination()]
});