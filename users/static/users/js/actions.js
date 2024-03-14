async function handlePost(e) {
    e.preventDefault();

    showSwalLoading();

    const modal = $('#createModal');
    const form = $('#formCreate');

    const first_name = form.find('#first_name').val();
    const last_name = form.find('#last_name').val();
    const username = form.find('#username').val();
    const notelp = form.find('#nomor_telepon').val();
    const email = form.find('#email').val();
    const satker = form.find('#satker').val();

    const data = { first_name, last_name, username, notelp, email, satker };

    console.log('Data :', data);

    try {
        const response = await axios.post('/dashboard/users/api/v1/users/', data);

        if (!checkStatus(response.status, '2')) {
            throw new Error('Terjadi kesalahan saat menyimpan data');
        }

        showSwalSuccess('Berhasil', `Data pengguna telah berhasil <b>ditambahkan</b>`);

        modal.modal('hide');

        form.trigger('reset');
        form.find(`#satker`).val('').trigger('change');

        reloadTable(table);

        toast('success', 'Berhasil', `Data akun telah dikirimkan ke alamat email ${data.email}`);
    } catch (error) {
        console.log('Terjadi kesalahan : ', error);
        showSwalGenericError();
    }
}

async function handleEdit(id) {
    const modal = $('#editModal');
    const form = modal.find('#formUpdate');

    modal.modal('show');

    const response = await axios.get(`/dashboard/users/api/v1/users/${id}/`);

    block(form);

    const data = response.data;

    modal.find('#target_edited').html(data.profile.detail_satker.nama_satker);
    form.find('#edited_id').val(id);

    // Form
    form.find('#edited_first_name').val(data.first_name);
    form.find('#edited_last_name').val(data.last_name);
    form.find('#edited_username').val(data.username);
    form.find('#edited_nomor_telepon').val(data.profile.notelp);
    form.find('#edited_email').val(data.email);
    form.find('#edited_satker').val(data.profile.detail_satker.id).trigger('change');

    if (data.is_active) {
        form.find('#edited_status').prop('checked', true);
    } else {
        form.find('#edited_status').prop('checked', false);
    }

    await sleep(500);

    unblock(form);
}

async function handleUpdate(e) {
    e.preventDefault();

    showSwalLoading();

    const modal = $('#editModal');
    const form = $('#formUpdate');

    let id = form.find('#edited_id').val();
    let first_name = form.find('#edited_first_name').val();
    let last_name = form.find('#edited_last_name').val();
    let username = form.find('#edited_username').val();
    let notelp = form.find('#edited_nomor_telepon').val();
    notelp = notelp.replace(/ /g, '-');
    let email = form.find('#edited_email').val();
    let satker = form.find('#edited_satker').val();
    let edited_status = form.find('#edited_status').prop('checked');


    let is_active = false;
    if (edited_status) {
        is_active = true;
    }

    const user_id = id;

    const data = { first_name, last_name, username, notelp, email, satker, is_active, user_id };

    console.log('Payload : ', data);

    try {
        const response = await axios.patch(`/dashboard/users/api/v1/users/${id}/`, data);

        showSwalSuccess('Berhasil', `Data pengguna telah berhasil <b>diperbarui</b>`);

        console.log('Response : ', response);

        modal.modal('hide');

        reloadTable(table);
    } catch (error) {
        console.log('Terjadi kesalahan : ', error);
        showSwalGenericError();
    }
}

async function handleDelete(id) {
    const confirmation = await showSwalConfirm('Apakah anda yakin ingin menghapus data ini?');

    if (!confirmation.isConfirmed) return;

    showSwalLoading();

    try {
        const response = await axios.delete(`/dashboard/users/api/v1/users/${id}/`);

        showSwalSuccess('Berhasil', `Data pengguna telah berhasil <b>ditambahkan</b>`);

        reloadTable(table);

    } catch (error) {
        console.log('Terjadi kesalahan : ', error);
        showSwalGenericError();
    }
}

async function handleResetPassword(id, nama) {

    const confirmation = await showSwalConfirm(
        `Apakah anda yakin untuk <b>mereset</b> password dari pengguna <b>${nama}</b>?`,
        'Ya, reset password');

    if (!confirmation.isConfirmed) return;

    showSwalLoading();

    await sleep(1000);

    try {
        const response = await axios.post(`/accounts/api/reset-password/`, { user: id });

        showSwalSuccess('Berhasil',
            `Password dari user <b>${nama}</b> berhasil direset ke <b>123456</b> dan juga sudah dikirimkan <b>pesan pengingat</b> ke email bersangkutan.`,
            10000);

        await sleep(300);

        reloadTable(table);
    } catch (error) {
        console.log('Terjadi kesalahan : ', error);

        showSwalGenericError();
    }
}