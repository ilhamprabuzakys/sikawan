function validateExcel(e) {
    const fileInput = e.target;
    const file = e.target.files[0];

    if (!file) {
        showSwalError('Terjadi Kesalahan', `File anda gagal diupload. Tolong <b>upload</b> kembali.`);

        return;
    }

    const fileName = file.name;
    const fileExtension = fileName.split('.').pop().toLowerCase();

    if (!['csv', 'xls', 'xlsx'].includes(fileExtension)) {
        showSwalError('Terjadi Kesalahan',
            `File yang anda upload tidak sesuai format. Hanya file<b> CSV, XLS, atau XLSX</b> yang diperbolehkan.`
        );

        fileInput.value = '';

        return;
    }
};

function handleUnduhTemplate() { window.location.href = '/static/data/kawasan_rawan/Template Data Kawasan Rawan.csv'; }

async function handleAddKawasanRawan(e) {
    e.preventDefault();

    showSwalLoading();

    const form = $('#tambahForm');

    let tahun = form.find('#tahun').val();
    let desa = parseInt(form.find('#daftar_desa').val());
    let selected_nama_desa = $('#selected_kawasan').text();
    let status = form.find('#status').val();
    let keterangan = form.find('#keterangan').val() || null;

    const data = {
        tahun: tahun,
        desa: desa,
        status: status,
        keterangan: keterangan || null,
    };

    await sleep(1000);

    try {
        const response = await axios.post('/dashboard/masters/api/v1/kawasan_rawan/', data);

        console.log('Response : ', response);

        if (!checkStatus(response.status, '2')) {
            throw new Error('Terjadi kesalahan saat menyimpan data');
        }

        const response_data = response.data;

        if (response_data.info == 'updated') {
            const nama_desa = response_data.detail.nama_desa;
            const f_status = response_data.detail.status.from;
            const t_status = response_data.detail.status.to;

            showSwalSuccess('Berhasil', `Data <b>Kawasan Rawan</b> dari Kawasan <b>${nama_desa}</b><br>
            berhasil diperbarui dari status <b>${f_status}</b> ke <b>${t_status}</b>!`);
        } else {
            showSwalSuccess('Berhasil',
                `Data <b>Kawasan Rawan</b> untuk Kawasan <b>${selected_nama_desa}</b> telah berhasil ditambahkan!`
            );
        }
    } catch (error) {
        console.error('Terjadi kesalahan : ', error);
        showSwalGenericError();
    } finally {
        resetForm(form);
        form.find('#daftar_desa').empty();
        reloadTable(table);
        await handleRefetchData();
    }
};

/* ==========================
 * EXPORT DATA [XLSX, CSV]
============================= */
async function handleExportData(e) {
    e.preventDefault();

    const modal = $('#exportDataModal');
    const form = modal.find('#exportDataForm');
    const rekap_tahun = form.find('#export__tahun').val();
    const tipe_file = form.find('#export__tipe_file').val();

    let payload = { 'tahun': rekap_tahun, 'type': tipe_file };

    if (role == 'bnnp') {
        payload = { ...payload, id_provinsi };
    } else if (role == 'bnnk') {
        payload = { ...payload, id_kabupaten };
    }

    showSwalLoading();

    try {
        const response = await axios.post('/dashboard/masters/api/v1/desa_all_rawan/export/', payload);

        console.log('Response saat export', response);

        const data = response.data;

        if (!data.status) return;

        window.location.href = data.file;

        modal.modal('hide');

        const confirmation = await Swal.fire({
            title: "Berhasil",
            html: `Data Rekap Desa Kabupaten <br><b>${data.info.detail.nama}</b> tahun <b>${rekap_tahun}</b><br> telah <b>berhasil</b> digenerate! <br>Klik tombol unduh ulang apabila <b>gagal</b>!`,
            icon: "success",
            confirmButtonText: "Unduh ulang.",
            showCancelButton: true,
            cancelButtonText: 'Batalkan',
            showCloseButton: true,
            allowOutsideClick: false,
        });

        if (confirmation.isConfirmed) {
            console.log('Blud is downloading again!');
            window.location.href = data.file;
        }
    } catch (error) {
        console.error('Terjadi kesalahan :', error);
    }
}

/* ==========================
 * IMPORT DATA [XLSX, CSV]
============================= */
async function handleImportData(e) {
    e.preventDefault();
    console.log('Importing data ...');

    const modal = $('#importDataModal');
    const form = modal.find('#importDataForm');
    const tahun = form.find('#import__tahun').val();
    const file = form.find('#import__file')[0].files[0];
    const file_extension = file.name.split('.').pop();

    const formData = new FormData();

    formData.append('tahun', tahun);
    formData.append('tipe', role);
    formData.append('tipe_file', file_extension);
    formData.append('file', file);


    console.log('File:', file);

    showSwalLoading();

    try {
        const response = await axios.post('/dashboard/masters/api/v1/desa_all_rawan/import_data/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        console.log('Response : ', response);

        if (!response.data.status) return;

        const data = response.data;

        showSwalSuccess('Berhasil', `Data kawasan rawan untuk <br><b>${data.info.tipe}</b><br>dengan total data berjumlah telah <b>${data.info.total}</b> telah <b>berhasil</b> diimport`, 0);

        modal.modal('hide');

        form.find('#import__error_msg').addClass('d-none');
        reloadTable(table);
    } catch (error) {
        form.find('#import__file').val(null);

        const error_data = error.response.data;

        console.error('Terjadi kesalahan :', error_data.message);
        showSwalError('Terjadi Kesalahan', `Terjadi kesalahan saat mengimport data excel : <br><b>${error_data.message}</b>`);

        if (error_data.code == 'INVALID_FORMAT') {
            form.find('#import__error_msg').removeClass('d-none');
        }
    }
}
