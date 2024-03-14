$(function () {
    /***=======================================================
    * CREATE A NEW INSTANCE OF SELECT 2 USING ONLY A CLASSNAME
    ========================================================***/
    $("select:is(.select2)").each(function () {
        $(this).select2({
            theme: 'bootstrap-5',
            //placeholder: $(this).find('option:first').text(),
            dropdownParent: $(this).parent(),
            allowClear: false,
            language: {
                noResults: function () {
                    return `<span style="padding: 12px 15px">Hasil tidak ditemukan</span>`;
                },
            },
            escapeMarkup: function (markup) {
                return markup;
            }
        });

        // $(this).on('change', function () {
        //     var selectedValue = $(this).val();
        //     console.log("Nilai yang dipilih: " + selectedValue);
        // });
    });
});