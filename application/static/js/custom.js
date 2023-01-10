// FRONTEND
$(document).ready(function() {
	// SET WAKTU GLOBAL UNTUK LIBRARY MOMENT.JS KE INDONESIA
	moment.locale('id');
	$('#myTable').DataTable();
});

// tampil modal delete (halaman modelling)
$('.delete-modal').click(function() {
	$("#modelingDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
	$("#modelingDeleteModal").find("input[name='id']").val($(this).val());
	$('#modelingDeleteModal').modal('show');
});

//sidebar
$('#menu-action').click(function() {
	$('.sidebar').toggleClass('active');
	$('.main').toggleClass('active');
	$(this).toggleClass('active');
	
	if ($('.sidebar').hasClass('active')) {
		$(this).find('i').addClass('fa-close');
		$(this).find('i').removeClass('fa-bars');
	} else {
		$(this).find('i').addClass('fa-bars');
		$(this).find('i').removeClass('fa-close');
		$('ul .collapse').collapse('hide');
	}
});

// sidebar
$('#menu-action').hover(function() {
	$('.sidebar').toggleClass('hovered');
});

$("a[data-toggle='collapse']").click(function() {
	if (!$('.sidebar').hasClass('active')) {
		$('#menu-action').click();
	}
});

// mencetak total sample yang digunakan pada tampilan (modelling data [modal])
$('#sample-NONHS, #sample-HS, #sample-netral').on("change paste keyup", function() {
	const value = parseInt($(this).val());
	const max = parseInt($(this).attr('max'));

	if(value > 0 && value <= max) {
		$('#sample-NONHS, #sample-HS, #sample-netral').val(value);
		$('#total_sample').html(value * 2);
	}
	else {
		$('#sample-NONHS, #sample-HS, #sample-netral').val(max);
		$('#total_sample').html(max * 2);
	}
});

// validasi untuk tanggal pengambilan crawling awal
var min = new Date();
min.setDate(min.getDate()-7);
$('#tanggal_awal').attr('min', getHtmlDateString(min));
$('#tanggal_akhir').attr('min', getHtmlDateString(min));
$('#tanggal_awal').on("change paste keyup", function() {
	$('#tanggal_akhir').attr('min', $('#tanggal_awal').val());

	var date1 = new Date($(this).val());
	var date2 = new Date($('#tanggal_akhir').val());
	if(date1 > date2) {
		$('#tanggal_akhir').val($('#tanggal_awal').val());
	}
});

// validasi untuk tanggal pengambilan crawling akhir
var max = new Date();
max.setDate(max.getDate());
$('#tanggal_awal').attr('max', getHtmlDateString(max));
$('#tanggal_akhir').attr('max', getHtmlDateString(max));

// generate tanggal(yyy-mm-dd) berdasarkan parameter instance date
function getHtmlDateString(date) {
	var dd = date.getDate();
	var mm = date.getMonth()+1;
	var yyyy = date.getFullYear();
	if(dd<10){
		dd = '0'+dd;
	} 
	if(mm<10){
		mm = '0'+mm;
	}
	return yyyy+'-'+mm+'-'+dd;
}

// Mencari rasio data tes dan data latih
function cariRasio(kode) {
	$('#validasi_rasio').addClass('d-none');
	var jumlah_data = $('#jumlah_dataWithLabel').html();
	var rasio_hasil_testing = 0;
	var rasio_hasil_training = 0;

	if(kode == '1:9') {		// 1:9
		rasio_hasil_testing = Math.floor(jumlah_data * 0.1);
		rasio_hasil_training = Math.ceil(jumlah_data * 0.9);
		$('#rasio-satu-hasil').html('<i class="fa fa-arrow-right mr-3"></i>'+ rasio_hasil_testing +' Data Uji & '+ rasio_hasil_training +' Data Latih');
		$('#rasio-dua-hasil').empty();
	}
	else if(kode == '2:8') {		// 2:8
		rasio_hasil_testing = Math.floor(jumlah_data * 0.2);
		rasio_hasil_training = Math.ceil(jumlah_data * 0.8);
		$('#rasio-satu-hasil').html('<i class="fa fa-arrow-right mr-3"></i>'+ rasio_hasil_testing +' Data Uji & '+ rasio_hasil_training +' Data Latih');
		$('#rasio-dua-hasil').empty();
	}
}