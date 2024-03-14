var selected_tahun = $('#filter_statistik_tahun').val();

// Data total klasifikasi per tahun
const totalPerTahun = {
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
};

// Data provinsi placeholder
const selectedProvinsi = {
    id: 0,
    total_desa: 0,
    nama_provinsi: '',
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

var ctxPie = document.getElementById('pie-chart');
var ctxLine = document.getElementById('line-chart');

var pieChart = null;
var lineChart = null;

$(function () {
    (async () => {
        await fetchTotalKawasanRawan();
    })();
});

async function fetchTotalKawasanRawan() {
    block($('#line_chart_container'));
    block($('#pie_chart_container'));

    try {
        const response = await axios.get('/dashboard/masters/api/v1/total_kawasan_rawan/');

        console.log('Response : ', response);
        const data = response.data;

        // Set data total berdasarkan tahun
        data.forEach(item => {
            totalPerTahun[item.tahun].bahaya = item.bahaya;
            totalPerTahun[item.tahun].waspada = item.waspada;
            totalPerTahun[item.tahun].siaga = item.siaga;
            totalPerTahun[item.tahun].aman = item.aman;
            totalPerTahun[item.tahun].total = item.total;
        });

        await renderPieChart(totalPerTahun[selected_tahun].bahaya, totalPerTahun[selected_tahun].waspada, totalPerTahun[selected_tahun].siaga, totalPerTahun[selected_tahun].aman);
        await renderLineChart(getDataset('bahaya'), getDataset('waspada'), getDataset('siaga'), getDataset('aman'));
    } catch (error) {
        console.error('Terjadi kesalahan :', error)
    } finally {
        setDataKawasanRawan(totalPerTahun[selected_tahun].total, total_desa_indonesia);
        
        unblock($('#line_chart_container'));
        unblock($('#pie_chart_container'));

        return 'Statistik Total Sukses!'
    }
}

// Handle filter tahun
$('#filter_statistik_tahun').on('change', async function () {

    selected_tahun = $(this).val();

    const tahun_detail = `untuk tahun ke-${selected_tahun}`;
    const provinsi_detail = selectedProvinsi.id == 0 ? 'untuk satu INDONESIA' : `untuk provinsi ID-${selectedProvinsi.id}`
    console.log(`Filter ${tahun_detail} - ${provinsi_detail}`);

    // Provinsi semua
    if (selectedProvinsi.id == 0) {
        await renderPieChart(totalPerTahun[selected_tahun].bahaya, totalPerTahun[selected_tahun].waspada, totalPerTahun[selected_tahun].siaga, totalPerTahun[selected_tahun].aman);
        setDataKawasanRawan(totalPerTahun[selected_tahun].total, total_desa_indonesia);
    } else if (selectedProvinsi.id != 0) {
        // Spesifik provinsi
        setDataKawasanRawan(selectedProvinsi.kawasan_rawan[selected_tahun].total, selectedProvinsi.total_desa);
        await renderPieChart(selectedProvinsi.kawasan_rawan[selected_tahun].bahaya, selectedProvinsi.kawasan_rawan[selected_tahun].waspada, selectedProvinsi.kawasan_rawan[selected_tahun].siaga, selectedProvinsi.kawasan_rawan[selected_tahun].aman);
    }
});


function setDataKawasanRawan(jumlahTerisi, total) {
    $('#statistik_pelaporan_kawasan').text(jumlahTerisi); // Kawasan rawan yang terlaporkan
    $('#statistik_total_desa').text(total); // Dari total desa
}

async function saveProvinsiID() {
    selectedProvinsi.id = $('#filter_provinsi').val();

    // Jika memilih semua provinsi
    if (selectedProvinsi.id == 0) {
        await renderPieChart(totalPerTahun[selected_tahun].bahaya, totalPerTahun[selected_tahun].waspada, totalPerTahun[selected_tahun].siaga, totalPerTahun[selected_tahun].aman);

        setDataKawasanRawan(totalPerTahun[selected_tahun].total, total_desa_indonesia);

        return;
    }

    const response = await axios.get(`/dashboard/masters/api/v1/provinsi_all_rawan/?provinsi=${selectedProvinsi.id}`);

    const data = response.data.results[0];
    const all_kawasan = data.kawasan_rawan;

    Object.keys(all_kawasan).forEach(tahun => {
        selectedProvinsi.kawasan_rawan[tahun] = all_kawasan[tahun];
    });

    selectedProvinsi.total_desa = data.total_desa;
    selectedProvinsi.total_desa = data.total_desa;
    selectedProvinsi.nama_provinsi = data.nama_provinsi;

    console.log('selectedProvinsi :', selectedProvinsi);

    // Re-draw PieChart
    await renderPieChart(selectedProvinsi.kawasan_rawan[selected_tahun].bahaya, selectedProvinsi.kawasan_rawan[selected_tahun].waspada, selectedProvinsi.kawasan_rawan[selected_tahun].siaga, selectedProvinsi.kawasan_rawan[selected_tahun].aman);

    setDataKawasanRawan(selectedProvinsi.kawasan_rawan[selected_tahun].total, selectedProvinsi.total_desa);

    // Re-draw LineChart
    const line_datasets = {
        bahaya: [],
        waspada: [],
        siaga: [],
        aman: []
    };

    // const line_datasets.bahaya = [selectedProvinsi.kawasan_rawan['2021'].bahaya, selectedProvinsi.kawasan_rawan['2022'].bahaya, selectedProvinsi.kawasan_rawan['2023'].bahaya];

    // const line_datasets.waspada = [selectedProvinsi.kawasan_rawan['2021'].waspada, selectedProvinsi.kawasan_rawan['2022'].waspada, selectedProvinsi.kawasan_rawan['2023'].waspada];

    // const line_datasets.siaga = [selectedProvinsi.kawasan_rawan['2021'].siaga, selectedProvinsi.kawasan_rawan['2022'].siaga, selectedProvinsi.kawasan_rawan['2023'].siaga];

    // const line_datasets.aman = [selectedProvinsi.kawasan_rawan['2021'].aman, selectedProvinsi.kawasan_rawan['2022'].aman, selectedProvinsi.kawasan_rawan['2023'].aman];

    // Loop melalui setiap tahun dan mengisi array di dalam line_datasets
    Object.keys(selectedProvinsi.kawasan_rawan).forEach(tahun => {
        const data = selectedProvinsi.kawasan_rawan[tahun];
        line_datasets.bahaya.push(data.bahaya);
        line_datasets.waspada.push(data.waspada);
        line_datasets.siaga.push(data.siaga);
        line_datasets.aman.push(data.aman);
    });

    await renderLineChart(line_datasets.bahaya, line_datasets.waspada, line_datasets.siaga, line_datasets.aman);
}

async function renderPieChart(bahaya, waspada, siaga, aman) {
    const datasets = [bahaya, waspada, siaga, aman];

    block($('#pie_chart_container'));

    console.log('Rendering PieChart using : ', datasets);

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

    // Set text value
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

function getDataset(type) {
    const dataset = [];

    Object.keys(totalPerTahun).forEach(tahun => {
        dataset.push(totalPerTahun[tahun][type]);
    });

    return dataset;
}