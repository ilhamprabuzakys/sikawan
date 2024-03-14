const statistikData = {
    tahun: tahunSaatIni,
    total: 0,
    bahaya: 0,
    waspada: 0,
    siaga: 0,
    aman: 0,
};

$(function() {
    (async() => {
        await fetchStatistikSebaran();
        await setResults();
    })();
});

async function fetchStatistikSebaran() {
    block($('#statistik_pelaporan_kawasan_rawan'));
    const response = await axios.get('/dashboard/masters/api/v1/total_kawasan_rawan/');

    const data = response.data;

    const tahunData = data.find(item => item.tahun === statistikData.tahun);

    if (tahunData) {
        statistikData.total = tahunData.total;
        statistikData.bahaya = tahunData.bahaya;
        statistikData.waspada = tahunData.waspada;
        statistikData.siaga = tahunData.siaga;
        statistikData.aman = tahunData.aman;
    }

    unblock($('#statistik_pelaporan_kawasan_rawan'));
}

async function setResults() {
    $('.bahaya_count').text(statistikData.bahaya);
    $('.waspada_count').text(statistikData.waspada);
    $('.siaga_count').text(statistikData.siaga);
    $('.aman_count').text(statistikData.aman);
    $('#statistik_pelaporan_kawasan').text(statistikData.total);
}