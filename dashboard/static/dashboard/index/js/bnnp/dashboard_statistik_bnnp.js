var selected_tahun = $('#filter_statistik_tahun').val();

// Data provinsi placeholder
const dataStatistik = {
    id: id_provinsi,
    total_desa: total_desa_provinsi,
    nama_provinsi: nama_provinsi,
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

// Data kabupaten placeholder
const selectedKabupaten = {
    id: 0,
    total_desa: 0,
    nama_kabupaten: '',
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


var ctxPie = document.getElementById('pie-chart')
var ctxLine = document.getElementById('line-chart')

var pieChart = null;
var lineChart = null;

$('#filter_statistik_tahun').on('change', async function () {
    selected_tahun = $(this).val();

    const tahun_detail = `untuk tahun ke-${selected_tahun}`;
    const kecamatan_detail = selectedKabupaten.id == 0 ? 'untuk satu semua kabupaten' : `untuk kabupaten ID-${selectedKabupaten.id}`
    console.log(`Filter ${tahun_detail} - ${kecamatan_detail}`);

    // Kecamatan semua
    if (selectedKabupaten.id == 0) {
        await renderPieChart(dataStatistik.kawasan_rawan[selected_tahun].bahaya, dataStatistik.kawasan_rawan[selected_tahun].waspada, dataStatistik.kawasan_rawan[selected_tahun].siaga, dataStatistik.kawasan_rawan[selected_tahun].aman);

        setDataKawasanRawan(dataStatistik.kawasan_rawan[selected_tahun].total, dataStatistik.total_desa);
    } else if (selectedKabupaten.id != 0) {
        setDataKawasanRawan(selectedKabupaten.kawasan_rawan[selected_tahun].total, selectedKabupaten.total_desa);

        await renderPieChart(selectedKabupaten.kawasan_rawan[selected_tahun].bahaya, selectedKabupaten.kawasan_rawan[selected_tahun].waspada, selectedKabupaten.kawasan_rawan[selected_tahun].siaga, selectedKabupaten.kawasan_rawan[selected_tahun].aman);
    }
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

async function fetchAllRawanData() {
    block($('#line_chart_container'));
    block($('#pie_chart_container'));

    try {
        const response = await axios.get(`/dashboard/masters/api/v1/provinsi_all_rawan/?provinsi=${id_provinsi}`)

        console.log('Response :', response)

        const data = response.data.results[0];

        const all_kawasan = data.kawasan_rawan;

        Object.keys(all_kawasan).forEach(tahun => {
            dataStatistik.kawasan_rawan[tahun] = all_kawasan[tahun];
        });

        dataStatistik.total_desa = data.total_desa;

        await renderPieChart(dataStatistik.kawasan_rawan[selected_tahun].bahaya, dataStatistik.kawasan_rawan[selected_tahun].waspada, dataStatistik.kawasan_rawan[selected_tahun].siaga, dataStatistik.kawasan_rawan[selected_tahun].aman);
        await renderLineChart(getDataset('bahaya'), getDataset('waspada'), getDataset('siaga'), getDataset('aman'));
    } catch (error) {
        console.error('Terjadi kesalahan :', error)
    } finally {
        setDataKawasanRawan(dataStatistik.kawasan_rawan[selected_tahun].total, dataStatistik.total_desa);

        unblock($('#line_chart_container'));
        unblock($('#pie_chart_container'));

        return 'Statistik Sukses!'
    }
}

async function saveKabupatenID() {
    selectedKabupaten.id = $('#filter_kabupaten').val();

    // Jika memilih semua kabupaten
    if (selectedKabupaten.id == 0) {
        await renderPieChart(dataStatistik.kawasan_rawan[selected_tahun].bahaya, dataStatistik.kawasan_rawan[selected_tahun].waspada, dataStatistik.kawasan_rawan[selected_tahun].siaga, dataStatistik.kawasan_rawan[selected_tahun].aman);

        setDataKawasanRawan(dataStatistik.kawasan_rawan[selected_tahun].total, dataStatistik.total_desa);

        return;
    }

    const response = await axios.get(`/dashboard/masters/api/v1/kabupaten_all_rawan/?kabupaten=${selectedKabupaten.id}`);

    const data = response.data.results[0];
    const all_kawasan = data.kawasan_rawan;

    Object.keys(all_kawasan).forEach(tahun => {
        selectedKabupaten.kawasan_rawan[tahun] = all_kawasan[tahun];
    });

    selectedKabupaten.total_desa = data.total_desa;
    selectedKabupaten.nama_kabupaten = data.nama_kabupaten;
    selectedKabupaten.nama_provinsi = data.nama_provinsi;

    console.log('selectedKabupaten :', selectedKabupaten);

    // Re-draw PieChart
    await renderPieChart(selectedKabupaten.kawasan_rawan[selected_tahun].bahaya, selectedKabupaten.kawasan_rawan[selected_tahun].waspada, selectedKabupaten.kawasan_rawan[selected_tahun].siaga, selectedKabupaten.kawasan_rawan[selected_tahun].aman);

    setDataKawasanRawan(selectedKabupaten.kawasan_rawan[selected_tahun].total, selectedKabupaten.total_desa);

    // Re-draw LineChart
    const line_datasets = {
        bahaya: [],
        waspada: [],
        siaga: [],
        aman: []
    };

    // Loop melalui setiap tahun dan mengisi array di dalam line_datasets
    Object.keys(selectedKabupaten.kawasan_rawan).forEach(tahun => {
        const data = selectedKabupaten.kawasan_rawan[tahun];
        line_datasets.bahaya.push(data.bahaya);
        line_datasets.waspada.push(data.waspada);
        line_datasets.siaga.push(data.siaga);
        line_datasets.aman.push(data.aman);
    });

    await renderLineChart(line_datasets.bahaya, line_datasets.waspada, line_datasets.siaga, line_datasets.aman);
}


async function renderPieChart(bahaya, waspada, siaga, aman) {
    block($('#pie_chart_container'));
    
    const datasets = [bahaya, waspada, siaga, aman];
    
    console.log('Rendering PieChart using data :', datasets)

    if (pieChart) pieChart.destroy();

    pieChart = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: ['Bahaya', 'Waspada', 'Siaga', 'Aman'],
            datasets: [{
                data: datasets,
                backgroundColor: [danger, warning, light_primary, light_success]
            }]
        },
        options: {
            plugins: {
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = 0
                        let dataArr = ctx.chart.data.datasets[0].data
                        dataArr.map((data) => {
                            sum += data
                        })
                        let percentage = ((value * 100) / sum).toFixed(2) + '%'
                        return `${value} (${percentage})`
                    },
                    color: '#fff'
                }
            }
        }
    })

    $('.bahaya_count').text(bahaya);
    $('.waspada_count').text(waspada);
    $('.siaga_count').text(siaga);
    $('.aman_count').text(aman);

    unblock($('#pie_chart_container'));
}

async function renderLineChart(bahaya, waspada, siaga, aman) {
    block($('#line_chart_container'));

    if (lineChart) lineChart.destroy();

    console.log('Rendering LineChart using : ', {
        bahaya,
        waspada,
        siaga,
        aman
    });

    lineChart = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: [2021, 2022, 2023],
            // Bahaya
            datasets: [{
                    data: bahaya,
                    label: 'Bahaya',
                    borderColor: danger,
                    pointStyle: 'circle',
                    backgroundColor: danger,
                    fill: !1,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5,
                    pointBorderColor: danger
                },
                // Waspada
                {
                    data: waspada,
                    label: 'Waspada',
                    borderColor: warning,
                    tension: 0.5,
                    pointStyle: 'circle',
                    backgroundColor: warning,
                    fill: !1,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5
                },
                // Siaga
                {
                    data: siaga,
                    label: 'Siaga',
                    borderColor: primary,
                    tension: 0.5,
                    pointStyle: 'circle',
                    backgroundColor: primary,
                    fill: !1,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5,
                    pointBorderColor: 'transparent',
                    pointHoverBorderColor: primary,
                    pointHoverBackgroundColor: primary
                },
                // Aman
                {
                    data: aman,
                    label: 'Aman',
                    borderColor: success,
                    tension: 0.5,
                    pointStyle: 'circle',
                    backgroundColor: success,
                    fill: !1,
                    pointRadius: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderWidth: 5,
                    pointBorderColor: 'transparent',
                    pointHoverBorderColor: success,
                    pointHoverBackgroundColor: success
                }
            ]
        }
    });

    unblock($('#line_chart_container'));
}

function setDataKawasanRawan(jumlahTerisi, total) {
    $('#statistik_pelaporan_kawasan').text(jumlahTerisi); // Kawasan rawan yang terlaporkan
    $('#statistik_total_desa').text(total); // Dari total desa
}

function getDataset(type) {
    const dataset = [];

    Object.keys(dataStatistik.kawasan_rawan).forEach(tahun => {
        dataset.push(dataStatistik.kawasan_rawan[tahun][type]);
    });

    return dataset;
}