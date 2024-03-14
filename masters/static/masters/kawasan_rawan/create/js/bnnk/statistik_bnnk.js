// Passing ke variabel baru agar tidak konflik dengan filter tahun yang ada di DT
var filter_statistik_tahun_val = selected_tahun;

// Data kabupaten placeholder
const dataStatistik = {
    id: id_kabupaten,
    total_desa: total_desa_kabupaten,
    nama_kabupaten: nama_kabupaten,
    kawasan_rawan: {
        '2021': {
            bahaya: 0,
            waspada: 0,
            siaga: 0,
            aman: 0,
            total: 0
        },
        '2022': {
            bahaya: 0,
            waspada: 0,
            siaga: 0,
            aman: 0,
            total: 0
        },
        '2023': {
            bahaya: 0,
            waspada: 0,
            siaga: 0,
            aman: 0,
            total: 0
        }
    }
};

$(function () {
    $('#filter_statistik_tahun').on('change', async function () {
        filter_statistik_tahun_val = $(this).val();

        await setResultText();
    });
});


$(function () {
    (async () => {
        try {
            await fetchAllRawanData();
        } catch (error) {
            console.error('Terjadi kesalahan saat memuat data statistik :', error);
        }
    })();
});

async function handleRefetchData() {
    await fetchAllRawanData();
}

async function fetchAllRawanData() {
    block($('#statistik_pelaporan_kawasan_rawan'));
    block($('#statistik_pelaporan_kawasan'));

    try {
        const response = await axios.get(`/dashboard/masters/api/v1/kabupaten_all_rawan/?kabupaten=${id_kabupaten}`)

        const data = response.data.results[0];

        const all_kawasan = data.kawasan_rawan;

        Object.keys(all_kawasan).forEach(tahun => {
            dataStatistik.kawasan_rawan[tahun] = all_kawasan[tahun];
        });

        dataStatistik.total_desa = data.total_desa;
        dataStatistik.nama_kabupaten = data.nama_kabupaten;

        await setResultText();
        
    } catch (error) {
        console.error('Terjadi kesalahan :', error)
    } finally {
        unblock($('#statistik_pelaporan_kawasan'));
        unblock($('#statistik_pelaporan_kawasan_rawan'));

        return 'Statistik Sukses!'
    }
}


async function setResultText() {
    $('.bahaya_count').text(dataStatistik.kawasan_rawan[filter_statistik_tahun_val].bahaya);
    $('.waspada_count').text(dataStatistik.kawasan_rawan[filter_statistik_tahun_val].waspada);
    $('.siaga_count').text(dataStatistik.kawasan_rawan[filter_statistik_tahun_val].siaga);
    $('.aman_count').text(dataStatistik.kawasan_rawan[filter_statistik_tahun_val].aman);

    $('#statistik_pelaporan_kawasan').text(dataStatistik.kawasan_rawan[filter_statistik_tahun_val].total);
}

async function fetchStatistikData() {

    block($('#statistik_pelaporan_kawasan_rawan'));
    block($('#statistik_pelaporan_kawasan'));

    try {
        const response = await axios.get(`/dashboard/masters/api/v1/provinsi_rawan/?tahun=${filter_statistik_tahun_val}&provinsi=${id_provinsi}`)

        console.log('Response :', response)

        if (response.data.length == 0) return

        const data = response.data[0];

        jumlah_data_bahaya = data.bahaya
        jumlah_data_waspada = data.waspada
        jumlah_data_siaga = data.siaga
        jumlah_data_aman = data.aman

        jumlah_data_total = jumlah_data_bahaya + jumlah_data_waspada + jumlah_data_siaga + jumlah_data_aman;

        $('.bahaya_count').text(jumlah_data_bahaya);
        $('.waspada_count').text(jumlah_data_waspada);
        $('.siaga_count').text(jumlah_data_siaga);
        $('.aman_count').text(jumlah_data_aman);
        $('#statistik_pelaporan_kawasan').text(jumlah_data_total);
    } catch (error) {
        console.error('Terjadi kesalahan :', error)
    } finally {
        unblock($('#statistik_pelaporan_kawasan'));
        unblock($('#statistik_pelaporan_kawasan_rawan'));

        return 'Statistik Sukses!'
    }
}