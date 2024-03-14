var s = '';

var filter = {
	satker_bnnp: 0,
	satker_bnnk: 0,
	provinsi: 0,
	kabupaten: 0,
	status: '',
};

const semua_option = `<option value="">Semua</option>`;


function getURL() {
	let modified_url = `/dashboard/users/api/v1/users/?format=datatables`;

	if (s !== '') {
		s = convertToTitleCaseAndReplaceSpace(s);
		modified_url += `&s=${s}`;
	}
	if (filter.satker_bnnp && filter.satker_bnnp != 0) {
		modified_url += `&satker=${filter.satker_bnnp}`;
	}
	if (filter.satker_bnnk && filter.satker_bnnk != 0) {
		modified_url += `&satker=${filter.satker_bnnk}`;
	}
	if (filter.provinsi && filter.provinsi != 0) {
		modified_url += `&asal_provinsi=${filter.provinsi}`;
	}
	if (filter.kabupaten && filter.kabupaten != 0) {
		modified_url += `&asal_kabupaten=${filter.kabupaten}`;
	}
	if (filter.status != '') {
		modified_url += `&is_active=${filter.status}`;
	}
	return modified_url;
}

$(function () {
	let timeoutId;

	$('#__table_wrapper input[type="search"]').on('keyup', function () {
		clearTimeout(timeoutId);

		timeoutId = setTimeout(function () {
			s = $(this).val();

			let url = getURL();

			console.log('URL:', url);

			table.ajax.url(url).load();
		}.bind(this), 500);
	});
});

function handleApplyFilter() {
	const form = $('#filter_form');

	filter.satker_bnnp = form.find('#filter_satker_bnnp').val();
	filter.satker_bnnk = form.find('#filter_satker_bnnk').val();
	filter.provinsi = form.find('#filter_provinsi').val();
	filter.kabupaten = form.find('#filter_kabupaten').val();
	filter.status = form.find('#filter_status').val();

	let url = getURL();

	console.log('URL:', url);

	table.ajax.url(url).load();
}

function handleResetFilter() {
	const form = $('#filter_form');

	form.find('#filter_satker_bnnp').val('').trigger('change');
	form.find('#filter_satker_bnnk').val('').trigger('change');
	form.find('#filter_provinsi').val('').trigger('change');
	form.find('#filter_kabupaten').val('').trigger('change');
	form.find('#filter_status').val('');

	filter.satker_bnnp = 0;
	filter.satker_bnnk = 0;
	filter.provinsi = 0;
	filter.kabupaten = 0;
	filter.status = '';

	let url = getURL();

	console.log('URL:', url);

	table.ajax.url(url).load();
}

async function loadKabupaten(provinsiId) {
	const kabupatenDropdown = $('#filter_kabupaten');

	if (!provinsiId) return;

	resetKabupaten();

	try {
		const response = await axios.get(`/dashboard/masters/api/v1/list_regencies/?provinsi=${provinsiId}`);

		response.data.forEach(kabupaten => {
			kabupatenDropdown.append($('<option>', {
				value: kabupaten.id,
				text: kabupaten.nama_kabupaten
			}));
		});

		kabupatenDropdown.removeAttr('disabled');
	} catch (error) {
		console.error('Error:', error);
	}
}

function resetKabupaten() {
	$('#filter_kabupaten').empty();
	$('#filter_kabupaten').append($('<option>', {
		value: '',
		text: '--Pilih Kota/Kabupaten--',
		disabled: true,
	}));
	$('#filter_kabupaten').prop('disabled', true);
	$('#filter_kabupaten').append(semua_option);
}

$('#filter_provinsi').change(async function () {
	const selectedProvinsiVal = $(this).val();

	if (selectedProvinsiVal && selectedProvinsiVal != '' && selectedProvinsiVal != null) {
		await loadKabupaten(selectedProvinsiVal);
	} else {
		resetKabupaten();
	}
});
