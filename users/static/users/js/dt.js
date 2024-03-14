const columns = [{
        data: null,
    },
    {
        data: 'first_name',
        render: function (data, type, row) {
            return `<div class="text-center"><span class="">${data}</span></div>`;
        }
    },
    {
        data: 'username',
        render: function (data, type, row) {
            return `<div class="text-center"><span class="">${data}</span></div>`;
        }
    },
    {
        data: 'email',
        render: function (data, type, row) {
            let email = data;
            if (email == '' || email == null) {
                email = 'Kosong';
            }
            return `<div class="text-center"><span class="">${email}</span></div>`;
        }
    },
    {
        data: 'profile.detail_satker.nama_satker',
        render: function (data, type, row) {
            return `<div class="text-center"><span class="">${data}</span></div>`;
        }
    },
    {
        data: 'is_active',
        render: function (data, type, row) {
            const list_of_status = [
                `<span class="btn btn-success rounded-0 text-white">Aktif</span>`,
                `<span class="btn btn-danger rounded-0 text-white">Tidak Aktif</span>`,
            ];

            let status_index = 0;

            if (!data) {
                status_index = 1;
            }

            return `<div class="text-center">${list_of_status[status_index]}</div>`;
        }
    },
    {
        data: 'id',
        render: function (data, type, row) {
            let nama_user = row.first_name;

            return `
            <div class="list-button gx-3 text-uppercase">
                <div>
                    <a href="javascript:void(0);" onclick="handleResetPassword(${data}, '${nama_user}')"
                        class="badge bg-primary text-white text-decoration-none mb-1"><i
                            class="fas fa-xmark me-2"></i>Reset Password</a>
                </div>
                <div>
                    <a href="javascript:void(0);" onclick="handleEdit(${data})"
                        class="badge bg-success text-white text-decoration-none mb-1"><i
                            class="fas fa-pen-to-square me-2"></i>Edit</a>
                </div>
                <div>
                    <a href="javascript:void(0);" class="badge bg-danger text-white text-decoration-none mb-1" onclick='handleDelete(${data})'><i
                            class="fas fa-trash-alt me-2"></i>Hapus</a>
                </div>
            </div>
        `;
        }
    },

];

var table = $('#__table').DataTable({
    language: dt_lang_config(),
    serverSide: true,
    searching: true,
    responsive: true,
    pageLength: 10,
    ajax: {
        url: `/dashboard/users/api/v1/users/?format=datatables`,
        dataSrc: 'data'
    },
    ordering: true,
    columns: columns,
    initComplete: function (settings, json) {
        console.log('Hasil fetch data : ', json);
    },
    columnDefs: [dt_row_pagination(), {
        "searchable": false,
        "targets": 5
    }]
});