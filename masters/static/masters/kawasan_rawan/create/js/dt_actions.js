async function handleDelete(id, nama_kawasan, tahun) {
    console.log(`Akan menghapus data kawasan rawan dari ID ${id} - Nama Kawasan ${nama_kawasan} pada tahun ke-${tahun}`);

    const confirmationText = `Apakah anda yakin ingin menghapus kawasan rawan untuk desa <b>${nama_kawasan}</b> tahun <b>${tahun}</b>` + '?';
    const confirm = await showSwalConfirm(confirmationText);

    if (!confirm.isConfirmed) {
        return;
    }

    showSwalLoading();

    try {
        const response = await axios.delete(`/dashboard/masters/api/v1/kawasan_rawan/${id}/`, {
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        });

        console.log(`Response ID: ${id}: `, response.data);

        showSwalSuccess('Berhasil', `Data kawasan rawan <b>${nama_kawasan}</b> untuk tahun <b>${tahun}</b>, <br>statusnya telah berhasil direset ke <b>Kosong</b>`);
    } catch (error) {
        console.log(`Terjadi kesalahan: `, error);
        showSwalGenericError();
    } finally {
        reloadTable(table);

        await handleRefetchData();
    }
}

async function handleDetail(id, tahun) {
    console.log(`Akan menampilkan detail kawasan rawan ID ${id} tahun ke-${tahun}`);

    const response = await axios.get(`/dashboard/masters/api/v1/kawasan_rawan/${id}/`);

    console.log(`Response saat fetch detail ID ${id}: `, response.data);
    const modal = $('#detailModal');

    const data = response.data;

    const wilayah = data.wilayah;

    const { nama_desa, nama_kecamatan, nama_kabupaten, nama_provinsi } = wilayah;

    const waktu = moment(data.created_at).format('HH:mm:ss - DD MMMM YYYY');
    const keterangan = data.keterangan == null ? '-' : data.keterangan;

    modal.find('.detail_desa').text(nama_desa);

    const lokasi = modal.find('ul.lokasi');

    lokasi.find('.detail_provinsi').text(nama_provinsi);
    lokasi.find('.detail_kabupaten').text(nama_kabupaten);
    lokasi.find('.detail_kecamatan').text(nama_kecamatan);

    const detail_pelapor = modal.find('ul.pelapor');

    const created_by = data.created_by;

    if (created_by) {
        const pelapor_nama = created_by.first_name + ' ' + created_by.last_name;
        const pelapor_username = created_by.username;
        const pelapor_email = created_by.email;
        const pelapor_notelp = created_by.profile.notelp;

        detail_pelapor.find('.detail_pelapor_nama').text(pelapor_nama == '' ? '-' : pelapor_nama);
        detail_pelapor.find('.detail_pelapor_username').text(pelapor_username == '' ? '-' : pelapor_username);
        detail_pelapor.find('.detail_pelapor_email').text(pelapor_email == '' ? '-' : pelapor_email);
        detail_pelapor.find('.detail_pelapor_notelp').text(pelapor_notelp == '' ? '-' : pelapor_notelp);
    }

    modal.find('.detail_status').removeClass().addClass("detail_status text-capitalize");
    modal.find('.detail_status').text(`${data.status}`);
    modal.find('.detail_status').addClass('text-' + getStatusClass(data.status));

    modal.find('.detail_waktu').text(waktu);
    modal.find('.detail_tahun').text(tahun);
    modal.find('.detail_desa_tahun').text(tahun);
    modal.find('.detail_keterangan').text(keterangan);

    modal.modal('show');
}

async function handleEdit(id, tahun, type='kawan') {
    hideAllModal();
    // Jika typenya bukan kawan kita show desa biasa, agar ia bisa menginputkan status dan keterangannya secara langsung.
    console.log(`Type : ${type} - Edit ID ${id} tahun ${tahun}`);

    let apiURL = '';
    let id_kawan = null;
    let id_desa = null;

    if (type == 'kawan') {
        apiURL = `/dashboard/masters/api/v1/kawasan_rawan/${id}/`;
        id_kawan = id;
        id_desa = 0;
    } else {
        apiURL = `/dashboard/masters/api/v1/desa/${id}/`;
        id_desa = id;
        id_kawan = 0;
    }

    const response = await axios.get(apiURL);

    console.log(`Response saat fetch detail untuk edit ID ${id}: `, response.data);
    const modal = $('#editModal');
    const form = modal.find('#formUpdate');

    const data = response.data;

    let desa = '';
    let kecamatan = '';
    let kabupaten = '';
    let provinsi = '';
    let status = '-';
    let waktu = '-';
    let keterangan = '-';

    if (type == 'kawan') {
        const wilayah = data.wilayah;

        desa = wilayah.nama_desa;
        kecamatan = wilayah.nama_kecamatan;
        kabupaten = wilayah.nama_kabupaten;
        provinsi = wilayah.nama_provinsi;

        status = data.status;
        waktu = moment(data.created_at).format('HH:mm:ss - DD MMMM YYYY');
        keterangan = data.keterangan;
    } else {
        desa = data.nama_desa;
        kecamatan = data.nama_kecamatan;
        kabupaten = data.nama_kabupaten;
        provinsi = data.nama_provinsi;
    }

    modal.find('.detail_desa').text(desa);
    modal.find('.detail_desa_tahun').text(tahun);
    modal.find('#edited_desa_id').val(id_desa);
    modal.find('#edited_kawan_id').val(id_kawan);

    const lokasi = modal.find('ul.lokasi');

    lokasi.find('.detail_provinsi').text(provinsi);
    lokasi.find('.detail_kabupaten').text(kabupaten);
    lokasi.find('.detail_kecamatan').text(kecamatan);

    modal.find('.detail_status').removeClass().addClass("detail_status text-capitalize");
    modal.find('.detail_status').text(`${status}`);
    modal.find('.detail_status').addClass('text-' + getStatusClass(status));

    modal.find('.detail_tahun').text(tahun);
    modal.find('.detail_waktu').text(waktu);

    modal.find('.detail_keterangan').text(keterangan ?? '-');

    form.find('#edit_status_kerawanan').val(status).trigger('change');
    form.find('#edit_keterangan').val(keterangan);

    modal.modal('show');
}

async function handleUpdate(e) {
    e.preventDefault();

    showSwalLoading();

    const modal = $('#editModal');
    const form = $('#formUpdate');

    let id_kawan = form.find('#edited_kawan_id').val();
    console.log('Akan mengupdate data kawasan rawan ID-', id_kawan);

    let status = form.find(`#edit_status_kerawanan`).val();
    let keterangan = form.find('#edit_keterangan').val();

    let tahun = modal.find('.detail_tahun').text();
    let desa = modal.find('#edited_desa_id').val();

    const data = { status, keterangan };

    console.log('Data yang akan dikirim : ', data);

    try {
        let response = null;
        let response_text = '';

        if (id_kawan != 0) {
            response = await axios.patch(`/dashboard/masters/api/v1/kawasan_rawan/${id_kawan}/`, data);
            response_text = 'perbarui';
        } else {
            let data_post = { status, keterangan, tahun, desa };

            response = await axios.post(`/dashboard/masters/api/v1/kawasan_rawan/`, data_post);

            response_text = 'simpan';
        }

        console.log('Response : ', response);

        if (!String(response.status).startsWith('2')) {
            throw new Error('Terjadi kesalahan saat menyimpan data');
        }

        showSwalSuccess('Berhasil', `Data kawasan rawan telah berhasil <b>${response_text}</b>`);
    } catch (error) {
        console.log('Terjadi kesalahan : ', error);
        showSwalGenericError();
    } finally {
        modal.modal('hide');
        reloadTable(table);
        await handleRefetchData();
    }
}

function handleShowMore(element) {
    console.log('Show more ...');
    $(element).closest('.text-center').removeClass('d-block').addClass('d-none');
    $(element).closest('td').find('.full-text').removeClass('d-none').addClass('d-block');
    $(element).closest('td').find('.show-less').removeClass('d-none').addClass('d-block');
}

function handleShowLess(element) {
    console.log('Show less ...');
    $(element).closest('.show-less').addClass('d-none');
    $(element).closest('td').find('.full-text').removeClass('d-block').addClass('d-none');
    $(element).closest('td').find('.text-center').removeClass('d-none').addClass('d-block');
    $(element).closest('td').find('.show-more').removeClass('d-none').addClass('d-block');
}