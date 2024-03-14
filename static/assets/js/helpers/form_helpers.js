// Label
document.querySelectorAll("label.required").forEach((label) => {
    const supElement = document.createElement("sup");
    supElement.className = "ms-0-15r text-danger";
    supElement.textContent = "*";

    label.appendChild(supElement);
});

document.querySelectorAll("label.optional").forEach((label) => {
    const supElement = document.createElement("span");
    supElement.className = "ms-2 text-muted";
    supElement.textContent = "(Opsional)";

    label.appendChild(supElement);
});


function resetFormOld(form) {
    console.log('Terpanggil 2 Resetting this form :', form);

    if (!$(form).hasClass('dont-reset') && !$(form).hasClass('filter-form')) {
        console.log('Resetting this form :', form);
        $(form).find('.select2').each(function () {
            console.log('Terdapat select2');
            let isMultiple = $(this).prop('multiple');
            $(this).val(isMultiple ? [] : '').trigger('change');
        });

        form.reset();
    }
}


/* ==========================
 * FORM RESET FUNCTIONALLITY
============================= */
$(function () {
    // Reset
    function resetForm(form) {
        if (form.hasClass('dont-reset') || form.hasClass('filter-form')) {
            console.log('Form not resetted because it\'s forbidden ...');
            return;
        }

        form.find('.select2').val(null).trigger('change');
        form.find('input[type="text"]').val('');
        form.find('input[type="checkbox"]').prop('checked', false);
        form.find('input[type="file"]').val(null);

        form.trigger('reset');
    }

    $('.modal').on('hidden.bs.modal', function () {
        const form = $(this).find('form');
        console.log('Form awal :', form);

        if (form) {
            console.log('Form direset dengan form:', form);
            resetForm(form);
        }
    });

    $('[type="reset"]').on('click', function () {
        let form = $(this).closest('form')[0];
        if (!form) return;
        resetForm(form);
    });
});

// Cleave
if (window.Cleave) {
    // Phone number
    let phone = document.querySelector('.cleave-phone');
    phone && new Cleave(phone, {
        phone: true,
        phoneRegionCode: "ID",
        phoneMaxLength: 14,
    });
}

// Max min
if ($('.input-maxlength').attr("maxlength")) {
    $('.input-maxlength').each(function () {
        $(this).maxlength({
            validate: !0,
            threshold: $(this).attr("maxlength"),
        });
    });
}
