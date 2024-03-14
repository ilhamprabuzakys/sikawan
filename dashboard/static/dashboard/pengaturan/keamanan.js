async function handleUpdatePassword(e) {
    e.preventDefault();

    const form = $('#formUpdatePassword');

    let current_password = form.find('#current_password').val().trim();
    let new_password = form.find('#new_password').val().trim();
    let new_password2 = form.find('#new_password2').val().trim();

    clearValidationErrors();

    // const statusValidation = validatePassword(new_password, new_password2);

    // if (!statusValidation) {
    //     return;
    // }

    const data = {
        current_password,
        new_password
    };

    console.log('Data : ', data);

    showSwalLoading();

    await sleep(1000);

    try {

        const response = await axios.post(`/accounts/api/update-password/`, data, {
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
        });

        console.log('Response : ', response);

        showSwalSuccess('Berhasil', `Password anda telah berhasil <b>diperbarui</b>`);

        form.trigger('reset');

    } catch (error) {
        console.error('Terjadi kesalahan : ', error);

        showSwalError('Terjadi kesalahan',
            `Gagal memperbarui password dikarenakan. <br> <b>${error.response.data.error}</b>`, 0);
    }
}

function validatePassword(new_password, new_password2) {
    new_password = new_password.trim();
    new_password2 = new_password2.trim();

    // Validasi password
    if (new_password !== new_password2) {
        $('#new_password_confirmation_error').removeClass('d-none');
        return false;
    }

    if (new_password.length < 8) {
        showValidationError('#criteria_1');
        console.log('Password minimal harus memiliki 8 karakter.');
        return false;
    }

    if (!/[A-Z]/.test(new_password)) {
        showValidationError('#criteria_2');
        console.log('Password harus memiliki setidaknya 1 huruf besar.');
        return false;
    }

    if (!/\d/.test(new_password) || !/[!@#$%^&*]/.test(new_password)) {
        showValidationError('#criteria_3');
        console.log('Password harus memilik setidaknya 1 nomor dan 1 simbol.');
        return false;
    }

    return true;
}

function showValidationError(criteriaId) {
    $(criteriaId).addClass('text-danger');
}

function clearValidationErrors() {
    $('#criteria_1, #criteria_2, #criteria_3').removeClass('text-danger');
    $('#new_password_confirmation_error').addClass('d-none');
}