$(function () {
    let daftar_desa_url = '';
    if (role == 'bnnp') {
        daftar_desa_url = `/dashboard/masters/api/v1/daftar_desa/?provinsi=${id_provinsi}`;
    } else if (role == 'bnnk') {
        daftar_desa_url = `/dashboard/masters/api/v1/daftar_desa/?kabupaten=${id_kabupaten}`;
    } else {
        daftar_desa_url = `/dashboard/masters/api/v1/daftar_desa/`;
    }

    /*
        async function loadKota(provinsiId) {
            const kotaDropdown = $('#kota');
            resetKota();
            resetKecamatan();
            resetKawasan();

            try {
                const response = await axios.get(
                    `/dashboard/masters/api/v1/list_regencies/?provinsi=${provinsiId}`, {
                        headers: {
                            'X-CSRFToken': getCSRFToken()
                        }
                    });

                response.data.results.forEach(kota => {
                    kotaDropdown.append($('<option>', {
                        value: kota.id,
                        text: kota.nama_kabupaten
                    }));
                });

                $('#kota').removeAttr('disabled');
            } catch (error) {
                console.error('Error:', error);
            }
        }
    */
   
    async function loadKecamatan(kotaId) {
        const kecamatanDropdown = $('#kecamatan');

        resetKecamatan();
        resetKawasan();

        try {
            const response = await axios.get(`/dashboard/masters/api/v1/list_districts/?kabupaten=${kotaId}`);

            response.data.results.forEach(kecamatan => {
                kecamatanDropdown.append($('<option>', {
                    value: kecamatan.id,
                    text: kecamatan.nama_kecamatan
                }));
            });

            $('#kecamatan').removeAttr('disabled');
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function loadKawasan(kecamatanId) {
        const kawasanDropdown = $('#kawasan');
        resetKawasan();

        try {
            const response = await axios.get(`/dashboard/masters/api/v1/list_villages/?kecamatan=${kecamatanId}`);

            const data = response.data.results;

            data.forEach(kawasan => {
                kawasanDropdown.append($('<option>', {
                    value: kawasan.id,
                    text: kawasan.nama_desa
                }));
            });

            $('#kawasan').removeAttr('disabled');
        } catch (error) {
            console.error('Error:', error);
        }
    }

    /*
        $('#provinsi').change(async function () {
            const selectedProvinsi = $(this).val();
            $('#selected_provinsi').text($('#provinsi option:selected').text());
            await loadKota(selectedProvinsi);
        });
    */

    $('#kota').change(async function () {
        const selectedKota = $(this).val();
        $('#selected_kota').text($('#kota option:selected').text());
        $('#selected_kota_label').text('');

        selectedKota && await loadKecamatan(selectedKota);
    });

    $('#kecamatan').change(async function () {
        const selectedKecamatan = $(this).val();
        console.log('ID Kecamatan : ', selectedKecamatan);
        $('#selected_kecamatan').text($('#kecamatan option:selected').text());
        await loadKawasan(selectedKecamatan);

    });

    $('#kawasan').change(async function () {
        $('#selected_kawasan').text($('#kawasan option:selected').text());
        console.log('ID Kawasan : ', $(this).val());
    });
    
    $('#daftar_desa').change(async function () {
        $('#selected_kawasan').text($('#daftar_desa option:selected').text());
        console.log('ID Kawasan : ', $(this).val());
    });

    $('#tahun').change(async function () {
        $('#selected_tahun').text($('#tahun option:selected').text());
    });

    $('#tambahDesa').click(function () {
        $('#tambahDesaModal').modal('show');
    });

    $("#daftar_desa").select2({
        allowClear: true,
        placeholder: "--Pilih kawasan --",
        minimumInputLength: 1,
        formatInputTooShort: "Tolong ketikkan pencarian",
        ajax: {
          url: daftar_desa_url,
          dataType: "json",
          delay: 250,
          // Mengirim parameter query
          data: function(params) {
            return {
              s: params.term,
            };
          },
          // Memproses hasil dari API
          processResults: function(data) {
            return {
              results: data.results.map(function(item) {
                return {
                  id: item.desa_id,
                  text: item.desa_lengkap,
                };
              }),
            };
          },
        },
    });
});

function resetKota() {
    $('#kota').empty();
    $('#kota').append($('<option>', {
        value: '',
        text: '--Pilih kota--',
    }));
    $('#kecamatan').prop('disabled', true);
}

function resetKecamatan() {
    $('#kecamatan').empty();
    $('#kecamatan').append($('<option>', {
        value: '',
        text: '--Pilih kecamatan--',
    }));
    $('#kawasan').prop('disabled', true);
}

function resetKawasan() {
    $('#kawasan').empty();
    $('#kawasan').append($('<option>', {
        value: '',
        text: '--Pilih kawasan--',
    }));
}

function resetForm() {
    $('#kota').val('').trigger('change');
    $('#status').val('').trigger('change');
    $('#tahun').val('').trigger('change');

    resetKecamatan();
    $('#kecamatan').prop('disabled', true);
    resetKawasan();

    $('#selected_kota_label').text('KAB/KOTA');
    $('#selected_kota').text('____');
    $('#selected_kecamatan').text('____');
    $('#selected_kawasan').text('____');
    $('#selected_tahun').text('____');
}