const columns = [{
        data: null
    },
    // Provinsi
    {
        data: 'nama_provinsi',
        render: function (data, type, row) {
            return `<span>${data}</span>`;
        }
    },
    // Total kawasan
    {
        data: 'total_desa',
        render: function (data, type, row) {
            return `<span>${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // Status data pelaporan (xx/total)
    {
        data: 'kawasan_rawan.2021.total',
        render: function (data, type, row) {
            return `<span>(${data}/${row['total_desa']})</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    {
        data: 'kawasan_rawan.2022.total',
        render: function (data, type, row) {
            return `<span>(${data}/${row['total_desa']})</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    {
        data: 'kawasan_rawan.2023.total',
        render: function (data, type, row) {
            return `<span>(${data}/${row['total_desa']})</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // Kawasan - Bahaya
    // 2021
    {
        data: 'kawasan_rawan.2021.bahaya',
        render: function (data, type, row) {
            return `<span class="text-danger">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2022
    {
        data: 'kawasan_rawan.2022.bahaya',
        render: function (data, type, row) {
            return `<span class="text-danger">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2023
    {
        data: 'kawasan_rawan.2023.bahaya',
        render: function (data, type, row) {
            return `<span class="text-danger">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // Kawasan - Waspada
    // 2021
    {
        data: 'kawasan_rawan.2021.waspada',
        render: function (data, type, row) {
            return `<span class="text-warning">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2022
    {
        data: 'kawasan_rawan.2022.waspada',
        render: function (data, type, row) {
            return `<span class="text-warning">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2023
    {
        data: 'kawasan_rawan.2023.waspada',
        render: function (data, type, row) {
            return `<span class="text-warning">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // Kawasan - Siaga
    // 2021
    {
        data: 'kawasan_rawan.2021.siaga',
        render: function (data, type, row) {
            return `<span class="text-primary">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2022
    {
        data: 'kawasan_rawan.2022.siaga',
        render: function (data, type, row) {
            return `<span class="text-primary">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2023
    {
        data: 'kawasan_rawan.2023.siaga',
        render: function (data, type, row) {
            return `<span class="text-primary">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // Kawasan - Aman
    // 2021
    {
        data: 'kawasan_rawan.2021.aman',
        render: function (data, type, row) {
            return `<span class="text-success">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2022
    {
        data: 'kawasan_rawan.2022.aman',
        render: function (data, type, row) {
            return `<span class="text-success">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
    // 2023
    {
        data: 'kawasan_rawan.2023.aman',
        render: function (data, type, row) {
            return `<span class="text-success">${data}</span><span class="ms-2 text-muted">desa</span>`;
        }
    },
];

var table = $('#__table').DataTable({
    language: dt_lang_config(),
    serverSide: true,
    responsive: true,
    pageLength: 10,
    searchDelay: 1000,
    ajax: {
        url: `/dashboard/masters/api/v1/provinsi_all_rawan/?format=datatables`,
        dataSrc: 'data'
    },
    ordering: true,
    columns: columns,
    initComplete: function (settings, json) {
        console.log('Hasil fetch data : ', json);
    },
    columnDefs: [dt_row_pagination()]
});