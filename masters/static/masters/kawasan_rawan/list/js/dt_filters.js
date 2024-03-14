/* ==========================
 * INFORMASI :
Apabila hendak mereset value itu ke ' ' dikasih string dengan 1 spasi, ini untuk pas selectedOption di htmlnya jadi si badge hijaunya tidak menghilang jadi kita kasih 1 spasi saja.
============================= */

var search = '';

const CURRENT_URL = window.location.pathname;

const semua_option = `<option value="">Semua</option>`;

const selectedElements = {
	provinsi: $('#info__selected a.provinsi'),
	kota: $('#info__selected a.kota'),
	kecamatan: $('#info__selected a.kecamatan')
};

const selectedTexts = {
	provinsi: '',
	kota: '',
	kecamatan: ''
};

const selectedValues = {
	provinsi: null,
	kota: null,
	kecamatan: null
};

async function loadKota(provinsiId) {
	const kotaDropdown = $('#filter__kabupaten');

	if (!provinsiId) return;

	resetKota();
	resetKecamatan();

	try {
		const response = await axios.get(`/dashboard/masters/api/v1/list_regencies/?provinsi=${provinsiId}`);

		response.data.forEach(kota => {
			kotaDropdown.append($('<option>', {
				value: kota.id,
				text: kota.nama_kabupaten
			}));
		});

		kotaDropdown.removeAttr('disabled');
	} catch (error) {
		console.error('Error:', error);
	}
}

async function loadKecamatan(kotaId) {
	const kecamatanDropdown = $('#filter__kecamatan');

	if (!kotaId) return;

	resetKecamatan();

	try {
		const response = await axios.get(`/dashboard/masters/api/v1/list_districts/?kabupaten=${kotaId}`);

		response.data.forEach(kecamatan => {
			kecamatanDropdown.append($('<option>', {
				value: kecamatan.id,
				text: kecamatan.nama_kecamatan
			}));
		});

		kecamatanDropdown.removeAttr('disabled');
	} catch (error) {
		console.error('Error:', error);
	}
}

function resetKota() {
	$('#filter__kabupaten').empty();
	$('#filter__kabupaten').append($('<option>', {
		value: '',
		text: '--Pilih kota--',
		disabled: true,
	}));
	$('#filter__kabupaten').prop('disabled', true);
	$('#filter__kecamatan').prop('disabled', true);

	$('#filter__kabupaten').append(semua_option);
}

function resetKecamatan() {
	$('#filter__kecamatan').empty();
	$('#filter__kecamatan').append($('<option>', {
		value: '',
		text: '--Pilih kecamatan--',
		disabled: true
	}));
	$('#filter__kecamatan').prop('disabled', true);
	$('#filter__kecamatan').append(semua_option);
}

$('#filter__provinsi').change(async function () {
	selectedValues.provinsi = $(this).val();

	selectedValues.kota = '';
	selectedTexts.kota = ' ';
	selectedValues.kecamatan = '';
	selectedTexts.kecamatan = ' ';

	const selectedOptionText = $('#filter__provinsi option:selected').text();
	selectedTexts.provinsi = selectedOptionText != '--Pilih provinsi--' ? selectedOptionText : ' '

	// Jika memilih "semua"
	if (selectedValues.provinsi != '' && selectedValues.provinsi != null) {
		await loadKota(selectedValues.provinsi);
	} else {
		resetKota();
		resetKecamatan();
	}
});

$('#filter__kabupaten').change(async function () {
	selectedValues.kota = $(this).val();
	selectedTexts.kota = $('#filter__kabupaten option:selected').text() != 'Semua' ? $('#filter__kabupaten option:selected').text() : ' ';

	// Reset selectedValues dan selectedTexts
	selectedValues.kecamatan = null;
	selectedTexts.kecamatan = ' ';
	await loadKecamatan(selectedValues.kota);
});

$('#filter__kecamatan').change(async function () {
	selectedValues.kecamatan = $(this).val();
	selectedTexts.kecamatan = $('#filter__kecamatan option:selected').text() != 'Semua' ? $('#filter__kecamatan option:selected').text() : ' ';
});

function handleApplyFilter() {
	validateLocation();

	console.log('Selected Texts:', selectedTexts);

	// selectedElements.provinsi.text(selectedTexts.provinsi != 'Semua' ? selectedTexts.provinsi : ' ');
	// selectedElements.kota.text(selectedTexts.kota);
	// selectedElements.kecamatan.text(selectedTexts.kecamatan);

	Object.keys(selectedTexts).forEach(key => {
		selectedElements[key].text(selectedTexts[key] != 'Semua' ? selectedTexts[key] : ' ');
	});

	console.log('Selected filter values :', selectedValues)

	const webUrl = getWebURL(); // Dapatkan URL web saat ini dengan filter yang disimpan
	console.log('Web URL:', webUrl);
	const dtUrl = getDataTableAPIURL();
	console.log('DT URL:', dtUrl);

	table.ajax.url(dtUrl).load();

	window.history.pushState(null, null, webUrl);
};

function handleResetFilter() {
	// Set value ke null
	// selectedValues.provinsi = null;
	// selectedValues.kota = null;
	// selectedValues.kecamatan = null;

	Object.keys(selectedValues).forEach(key => {
		selectedValues[key] = null;
	});

	resetText();
	validateLocation();

	console.log('Selected Texts:', selectedTexts);

	// selectedElements.provinsi.text(selectedTexts.provinsi != 'Semua' ? selectedTexts.provinsi : ' ');
	// selectedElements.kota.text(selectedTexts.kota);
	// selectedElements.kecamatan.text(selectedTexts.kecamatan);

	Object.keys(selectedTexts).forEach(key => {
		selectedElements[key].text(selectedTexts[key] != 'Semua' ? selectedTexts[key] : ' ');
	});

	$('#filter__provinsi').val('').trigger('change');
	$('#filter__status').val('').trigger('change');
	$('#filter__tahun').val('2023').trigger('change');

	const webUrl = getWebURL(); // Dapatkan URL web saat ini dengan filter yang disimpan
	console.log('Web URL:', webUrl);
	const dtUrl = getDataTableAPIURL();
	console.log('DT URL:', dtUrl);

	table.ajax.url(dtUrl).load();

	window.history.pushState(null, null, webUrl);
}

function resetText() {
	// selectedTexts.provinsi = ' ';
	// selectedTexts.kota = ' ';
	// selectedTexts.kecamatan = ' ';

	Object.keys(selectedTexts).forEach(key => {
		selectedTexts[key] = ' ';
	});
}

// Fungsi untuk memvalidasi lokasi yang dipilih
function validateLocation() {
	// if (selectedValues.provinsi == null) {
	//     selectedValues.provinsi = '';
	// }
	// if (selectedValues.kota == null) {
	//     selectedValues.kota = '';
	// }
	// if (selectedValues.kecamatan == null) {
	//     selectedValues.kecamatan = '';
	// }

	Object.keys(selectedValues).forEach(key => {
		if (selectedValues[key] == null) {
			selectedValues[key] = '';
		}
	});
}

function getWebURL() {
	let url = CURRENT_URL;
	let query = '';

	if (selectedValues.provinsi && selectedValues.provinsi != '') {
		query += `provinsi=${selectedValues.provinsi}&`;
	}
	if (selectedValues.kota && selectedValues.kota != '') {
		query += `kabupaten=${selectedValues.kota}&`;
	}
	if (selectedValues.kecamatan && selectedValues.kecamatan != '') {
		query += `kecamatan=${selectedValues.kecamatan}&`;
	}
	if (search && search != '') {
		query += `s=${search}&`;
	}

	if (query !== '') {
		query = '?' + query.slice(0, -1); // Hapus karakter '&' di akhir query
	}

	return url + query;
}

function getDataTableAPIURL() {
	let url = '/dashboard/masters/api/v1/desa/?format=datatables';

	if (selectedValues.provinsi && selectedValues.provinsi != '') {
		url += `&provinsi=${selectedValues.provinsi}`;
	}
	if (selectedValues.kota && selectedValues.kota != '') {
		url += `&kabupaten=${selectedValues.kota}`;
	}
	if (selectedValues.kecamatan && selectedValues.kecamatan != '') {
		url += `&kecamatan=${selectedValues.kecamatan}`;
	}
	if (search && search != '') {
		search = convertToTitleCaseAndReplaceSpace(search);
		url += `&s=${search}`;
	}

	return url;
}

$(function () {
	let timeoutId;

	$('#__table_wrapper input[type="search"]').on('keyup', function () {
		clearTimeout(timeoutId);

		timeoutId = setTimeout(function () {
			s = $(this).val();

			let url = getDataTableAPIURL();

			console.log('URL:', url);

			table.ajax.url(url).load();
		}.bind(this), 500);
	});
});