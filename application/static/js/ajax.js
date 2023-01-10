// AJAX - GET AND READ DATA SCRAPING
$('#crawling_data').click(function() {
	
	var flag = 0;
	var form_dataArray = $('form').serializeArray();

	// Validasi form input
	$('#validasi_kata_kunci').removeClass('d-none');
	$('#validasi_tanggal_awal').removeClass('d-none');
	$('#validasi_tanggal_akhir').removeClass('d-none');
	$('#validasi_tanggal_akhir_2').removeClass('d-none');
	if(form_dataArray[0]['value'].trim() != '') {
		flag += 1;
		$('#validasi_kata_kunci').addClass('d-none');
	}
	if(form_dataArray[1]['value'].trim() != '') {
		flag += 1;
		$('#validasi_tanggal_awal').addClass('d-none');
	}
	if(form_dataArray[2]['value'].trim() != '') {
		flag += 1;
		$('#validasi_tanggal_akhir').addClass('d-none');
	}
	if(form_dataArray[1]['value'].trim() <= form_dataArray[2]['value'].trim()) {
		flag += 1;
		$('#validasi_tanggal_akhir_2').addClass('d-none');
	}
	if(form_dataArray[3]['name'].trim() == 'aksi' && form_dataArray[3]['value'].trim() == 'crawling') {
		flag += 1;
	}

	// jika form input telah tervalidasi seluruhnya maka jalankan AJAX Request
	if(flag == 5) {
		var content =	"";
		$.ajax({
			url         : "/crawling",
			data		: $('form').serialize(),
			type        : "POST",
			dataType	: "json",
			beforeSend: function() {
				content +=	`
								<div class="bs-callout bs-callout-primary mt-0">
									<h4>Data <em>Crawling</em></h4>
									<p class="text-muted"><em>Crawling</em> Data dengan kata kunci <strong>`+ $('#kata_kunci').val() +`</strong>, dari tanggal <strong>`+ moment($('#tanggal_awal').val()).format("LL") +`</strong> s/d <strong>`+ moment($('#tanggal_akhir').val()).format("LL") +`</strong>.</p>
								</div>
								
								<div class="loaderDiv my-5 m-auto"></div>
							`;
							
				$('#content_crawling').html(content);
				$(".loaderDiv").show();
			},
			success     : function(response) {
				
				var total_dataDidapat = response.data_crawling.length;
				
				content +=	`
								<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
									<label class="text-center d-inline-flex align-items-center mb-1">
										<h3 class="text-info mb-1">`+ total_dataDidapat +`</h3>
										<span class="ml-2 text-muted"> Data didapat</span>
									</label>
									<form action="/crawling" method="POST">									
										<input type="hidden" name="aksi" value="save_crawling" required readonly />
										<button type="submit" class="btn btn-primary w-75"><i class="fa fa-save"></i> Simpan Data</button>
									</form>
								</div>
								<div class="table-responsive-sm">
									<table class="table table-bordered table-striped text-center" id="myTable">
										<thead>
											<tr>
												<th>No.</th>
												<th>ID</th>
												<th>Teks</th>
												<th>Pengguna</th>
												<th>Dibuat pada</th>
											</tr>
										</thead>
										<tbody>
							`;
							
				$.each(response.data_crawling, function(index, data) {
					content +=	`
											<tr>
												<td>`+ ++index +`</td>
												<td>`+ BigInt(data.id).toString() +`</td>
												<td class="text-left">`+ data.full_text +`</td>
												<td>`+ data.user.screen_name +`</td>
												<td>`+ moment(data.created_at).format("LLL") +`</td>
												
											</tr>
								`;
				});
	
				content += 	`
										</tbody>
									</table>
								</div>
							`;
				
				$('#content_crawling').html(content);
				
				$(".loaderDiv").hide();
				$('#myTable').DataTable();
				
				$('#modalCrawling').modal('toggle');
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
				
				$('#data_tes').on("keyup keypress change", function () {
					if($(this).val() > total_dataDidapat) {
						$(this).val(total_dataDidapat);
					}
					$('#data_latih').val(total_dataDidapat - $(this).val());
				});
				
				$('#data_latih').on("keyup keypress change", function () {
					if($(this).val() > total_dataDidapat) {
						$(this).val(total_dataDidapat);
					}
					$('#data_tes').val(total_dataDidapat - $(this).val());
				});
			},
			error     : function(x) {
				console.log(x.responseText);
			}
		});
	}
});

// AJAX - PROCESS AND READ DATA PREROCESSING
$('#preprocessing_data').click(function() {

	var form_dataArray = $('form').serializeArray();
	var jumlah_data_crawling = parseInt($('#jumlah_dataCrawling').html());
	
	// validasi data preprocessing
	if(jumlah_data_crawling > 0 && form_dataArray[0]['name'].trim() == 'aksi' && form_dataArray[0]['value'].trim() == 'preprocessing') {
		var content =	"";
		
		$.ajax({
			url         : "/preprocessing",
			data		: $('form').serialize(),
			type        : "POST",
			dataType	: "json",
			beforeSend: function() {		

				content +=	`
								<div class="bs-callout bs-callout-primary mt-0">
									<h4>Data <em>Preprocessing</em></h4>
									<p class="text-muted"><em>Preprocessing</em> <strong>`+ jumlah_data_crawling +`</strong> data <em>crawling</em></p>
								</div>
								
								<div class="loaderDiv my-5 m-auto"></div>
							`;
							
				$('#content_preprocessing').html(content);
				$(".loaderDiv").show();
			},
			success     : function(response) {
				content +=	`
								<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
									<label class="text-center d-flex justify-content-center align-items-center mb-0">
										<span class="mr-2 text-muted"> Berhasil melakukan <em>preprocessing</em>.</span>
										<div class="d-inline-flex align-items-center">
											<h3 class="text-info mb-0">`+ jumlah_data_crawling +`</h3>
											<span class="ml-2 text-muted"> Data telah disimpan!</span>
										</div>
									</label>
								</div>
								<div class="table-responsive-sm">
									<table class="table table-bordered table-striped text-center" id="myTable">
										<thead>
											<tr>
												<th>No.</th>
												<th>Teks Bersih</th>
												<th>Pilihan</th>
											</tr>
										</thead>
										<tbody>
							`;
							
				$.each(response.last_data, function(index) {
					content +=	`
											<tr>
												<td>`+ ++index +`</td>
												<td class="text-left">`+ response.last_data[--index] +`</td>
												<td class="text-center"><button class="btn btn-outline-info" data-toggle="modal" data-target="#modalDetailPreprocessing`+ index +`"><i class="fa fa-search-plus"></i> Detail</button></td>
											</tr>
											
											<div class="modal fade" id="modalDetailPreprocessing`+ index +`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
												<div class="modal-dialog modal-lg">
													<div class="modal-content">
														<div class="modal-header">
															<h5 class="modal-title" id="exampleModalLabel">Detail <em>Preprocessing</em> Tweet</h5>
															<button type="button" class="close" data-dismiss="modal" aria-label="Close">
															<span aria-hidden="true">&times;</span>
															</button>
														</div>
														<div class="modal-body px-5">
															<div class="row">
																<div class="col-md-12 d-flex justify-content-start align-items-center">
																	<div class="timeline">
																		<p><span>1. Tweet Awal</span><br />`+ response.first_data[index] +`</p>
																		<p><span>2. Case Folding</span><br />`+ response.case_folding[index]+`</p>
																		<p><span>3. Menghapus URL, Mention, Hastag, Selain Huruf, Spasi Berlebih (<em>Cleansing</em>)</span><br />`+ response.remove_non_character[index]+`</p>
																		<p><span>4. Mengubah kata tidak baku ke bentuk kata baku (<em>Slang Word</em>)</span><br />`+ response.change_slang[index]+`</p>
																		<p><span>5. Menghapus <em>Stop Word</em></span><br />`+ response.remove_stop_word[index]+`</p>
																		<p><span>6. Mengubah kata berimbuhan ke bentuk kata dasar (<em>Stemming</em>)</span><br />`+ response.change_stemming[index]+`</p>
																	</div>
																</div>
															</div>
														</div>
													</div>
												</div>
											</div>
								`;
				});
				
				content +=	`			</tbody>
									</table>
								</div>
								<div class="col-md-6 offset-md-3 col-sm-12 text-center">
									<a href="/preprocessing" class="btn btn-info w-50 text-decoration-none"><i class="fa fa-arrow-left"></i> Kembali</a>
								</div>
							`;
				
				$('#content_preprocessing').html(content);
				
				$(".loaderDiv").hide();
				$('#myTable').DataTable();
				
				$('#modalPreprocessing').modal('toggle');
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
			},
			error     : function(x) {
				console.log(x.responseText);
			}
		});
	} 
	else {
		$('#validasi_preprocessing').removeClass('d-none');
	}
});

// AJAX - LABELING DENGAN KAMUS
$('#labeling_kamus').click(function() {
	
	var form_dataArray = $('form').serializeArray();
	var jumlah_data_noLabel = parseInt($('#jumlah_dataNoLabel').html());

	// validasi data labeling kamus
	if(jumlah_data_noLabel > 0 && form_dataArray[0]['name'].trim() == 'aksi' && form_dataArray[0]['value'].trim() == 'labelingKamus') {
		var content =	"";
		
		$.ajax({
			url         : "/labeling_kamus",
			data		: $('form').serialize(),
			type        : "POST",
			dataType	: "json",
			beforeSend: function() {			
				content +=	`
								<div class="bs-callout bs-callout-primary mt-0">
									<h4><em>Labeling</em> Data</h4>
									<p class="text-muted"><em>Labeling</em> <strong>`+ jumlah_data_noLabel +`</strong> data berdasarkan teks bersih</p>
								</div>
								
								<div class="loaderDiv my-5 m-auto"></div>
							`;
							
				$('#content_labeling').html(content);
				$(".loaderDiv").show();
			},
			success     : function(response) {
				var sentimen_type = '';

				if(response.jumlah_netral > 0 && response.teks_data.length > 0) {
					content +=	`
									<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
										<label class="text-center mb-0">
											<p class="text-muted mb-0">Berhasil melakukan <em>labeling</em> pada</p>
											<p class="d-inline-flex align-items-center mb-0">
												<span class="text-info h3 mb-0 mr-2">`+ response.teks_data.length +`</span>
												<span class="text-muted"> Data dan telah disimpan!</span>
											</p>
											<hr />
											<p class="text-muted mb-0">Gagal melakukan <em>labeling</em> pada</p>
											<p class="text-muted mb-0"><span class="h6">`+ response.jumlah_netral +`</span> Data karena skor = 0.</p>
										</label>
									</div>
								`;
				}
				else if(response.jumlah_netral == 0 && response.teks_data.length > 0) {
					content +=	`
									<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
										<label class="text-center mb-0">
											<p class="text-muted mb-0">Berhasil melakukan <em>labeling</em>.</p>
											<p class="d-inline-flex align-items-center mb-0">
												<span class="text-info h3 mb-0 mr-2">`+ response.teks_data.length +`</span>
												<span class="text-muted"> Data telah disimpan!</span>
											</p>
										</label>
									</div>
								`;
				}
				else {
					content +=	`
									<div class="col-md-6 offset-md-3 col-sm-12 text-center border border-success rounded shadow py-4">
										<label class="text-center mb-0">
											<p class="text-muted mb-0">Gagal melakukan <em>labeling</em> pada</p>
											<p class="text-muted"><span class="h6">`+ response.jumlah_netral +`</span> Data karena skor = 0.</p>
											<small class="text-info">Silakan lakukan proses <em>labeling</em> secara manual.</small>
										</label>
									</div>
								`;
				}

				if(response.teks_data.length > 0) {
					content +=	`
									<div class="table-responsive-sm">
										<table class="table table-bordered table-striped text-center" id="myTable">
											<thead>
												<tr>
													<th>No.</th>
													<th>Teks Bersih</th>
													<th>Jumlah Kata NONHS</th>
													<th>Jumlah Kata HS</th>
													<th>Skor</th>
													<th><em>Label</em></th>
												</tr>
											</thead>
											<tbody>
								`;

					$.each(response.teks_data, function(index) {
					if(parseInt(response.skor_data[index]) > 0) {
						sentimen_type = '<label class="btn btn-success disabled">NONHS</label>';
					}
					else if(parseInt(response.skor_data[index]) == 0) {
						sentimen_type = '<label class="btn btn-secondary disabled">NETRAL</label>';
					}
					else {
						sentimen_type = '<label class="btn btn-danger disabled">HS</label>';
					}

					content +=	`
												<tr>
													<td>`+ ++index +`</td>
													<td class="text-left">`+ response.teks_data[--index] +`</td>
													<td class="text-center">`+ response.total_NONHS[index] +`</td>
													<td class="text-center">`+ response.total_HS[index] +`</td>
													<td class="text-center"><h6>`+ response.skor_data[index] +`</h6></td>
													<td class="text-center">`+ sentimen_type +`</td>
												</tr>
									`;
						});

					content +=	`			</tbody>
										</table>
									</div>
								`;
				}
				
				content += 	`
								<div class="col-md-6 offset-md-3 col-sm-12 text-center mt-3">
									<a href="/labeling" class="btn btn-info w-50 text-decoration-none"><i class="fa fa-arrow-left"></i> Kembali</a>
								</div>
							`;

				$('#content_labeling').html(content);
				
				$(".loaderDiv").hide();
				$('#myTable').DataTable();
				
				$('#modalPreprocessing').modal('toggle');
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
			},
			error     : function(x) {
				console.log(x.responseText);
			}
		});
	}
	else {
		$('#validasi_labelingKamus').removeClass('d-none');
	}
});

// AJAX - SPLIT DATA
$('#split_data').click(function() {
	
	var form_dataArray = $('form').serializeArray();
	var jumlah_data_with_label = parseInt($('#jumlah_dataWithLabel').html());
	
	// validasi data split
	$('#validasi_split').addClass('d-none');
	$('#validasi_rasio').addClass('d-none');
	if(jumlah_data_with_label > 0 && form_dataArray[0]['name'].trim() == 'rasio' && (form_dataArray[0]['value'] == '1:9' || form_dataArray[0]['value'] == '2:8')) {
		var content =	"";
		
		$.ajax({
			url         : "/split",
			data		: $('form').serialize(),
			type        : "POST",
			beforeSend: function() {
				content +=	`
								<br />
								<div class="modal-backdrop" style="background-color: rgba(0,0,0,0.3);"></div>
								<div class="loaderDiv my-5 m-auto"></div>
							`;
							
				$('#content_split').html(content);
				$(".loaderDiv").show();
			},
			success     : function(response) {
				if(response) {
					window.location = "/split";
				}
			},
			error     : function(x) {
				console.log(x.responseText);
			}
		});
	}
	else {
		if(jumlah_data_with_label <= 0) {
			$('#validasi_split').removeClass('d-none');
		}
		if(form_dataArray.length <= 1) {
			$('#validasi_rasio').removeClass('d-none');
		}
	}
});

// AJAX - MODEELING DATA
$('#modeling_data').click(function() {
	
	var form_dataArray = $('form').serializeArray();

	// validasi data modeling
	if(form_dataArray[0]['value'] > 0 && form_dataArray[0]['value'] == form_dataArray[1]['value']) {
		var content =	"";
		
		$.ajax({
			url         : "/modeling",
			data		: $('form').serialize(),
			type        : "POST",
			beforeSend: function() {
				content +=	`	
								<br />
								<div class="modal-backdrop" style="background-color: rgba(0,0,0,0.3);"></div>
								<div class="loaderDiv my-5 m-auto"></div>
							`;
							
				$('#content_modeling').html(content);
				$(".loaderDiv").show();
			},
			success     : function(response) {
				if(response.error) {
					content = response.error;
				}
				else {
					content = 	`
						<div class="col-md-8 offset-md-2 col-sm-12 text-center border border-success rounded shadow py-4 mb-4">
							<label class="text-center mb-0">
								<p class="mb-0 text-muted"> Berhasil melakukan <em>modeling</em>.</p>
								<p class="mb-0 text-muted"><em>Model</em> latih <span class="h6">`+ response.model_name +`</span> telah disimpan!</p>
							</label>
						</div>
						<div class="container-fluid text-mute">
							<h5>Komposisi data <em>model</em>:</h5>
							<pre>
	<span class="h6 text-dark">`+ response.model_name +`</span>
	└── <span class="h6">`+ response.sentiment_count +`</span> Data Latih
		├── <span class="h6 text-success">`+ response.sentiment_NONHS +`</span> bersentimen <span class="text-success">Non HS</span>
		└── <span class="h6 text-danger">`+ response.sentiment_HS +`</span> bersentimen <span class="text-danger">HS</span>
						</pre>
						</div>
					`;
					const data_dict = response.data_dict
					
					content += 	`
									<h5 class="container-fluid">6 sampel <em>tweet</em> pembangun <em>model</em>:</h5>
									<div class="table-responsive">	
										<table class="table table-sm table-bordered text-center">
											<thead>
												<tr>
													<th><em>Tweet</em></th>
													<th>Isi <em>Tweet</em> (<em>Clean Text</em>)</th>
												</tr>	
											</thead>
											<tbody>
								`;
					
					// for(let i=0; i<data_dict.teks_list.length; i++) {
					for(let i=0; i<6; i++) {
							content += 	`
												<tr>
													<td><em>Tweet</em> ke-`+ (i+1) +`</td>
													<td class="text-left">`+ data_dict.teks_list[i]+`</td>
												<tr>
										`;
					}


					content += 	`
													<td class="text-left pl-3" colspan="2"> .......... </td>
												</tr>
											</tbody>
										</table>
									</div>
									<br />
									<h5 class="container-fluid"> Vektor hasil CountVectorizer:</h5>
									<div class="table-responsive">	
										<table class="table table-sm table-bordered text-center">
											<thead>
												<tr>
													<th></th>
								`;
					for(let i=0; i<data_dict.unique_words.length; i++) {
						content += 	`<th><small>`+data_dict.unique_words[i]+`</small></th>`;
					}

					content += 	`				</tr>
											</thead>
											<tbody>
								`;
					// for(let i=0; i<data_dict.vector_list.length; i++) {
					for(let i=0; i<6; i++) {
						content += 	`
											<tr>
												<td class="text-left"><em>Tweet</em> ke-`+ (i+1) +`</td>
									`;
						for(let j=0; j<data_dict.unique_words.length; j++) {
								content += 	`	
												<td>`+ data_dict.vector_list[i][j] +`</td>
										`;
						}
						content += 	`
											<tr>
									`;
					}

					content += 	`				<tr>
													<td class="text-left pl-3" colspan="`+ data_dict.unique_words.length+1 +`"> .......... </td>
												</tr>
											</tbody>
										</table>
									</div>
									<div class="col-md-6 offset-md-3 col-sm-12 text-center mt-3">
										<a href="/modeling" class="btn btn-info w-50 text-decoration-none"><i class="fa fa-arrow-left"></i> Kembali</a>
									</div>
								`;
				}
				
				$('#content_modeling').html(content);
				
				$(".loaderDiv").hide();
				
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
			},
			error     : function(x) {
				console.log(x.responseText);
			}
		});
	}
	else {
		if(form_dataArray[0]['value'] != form_dataArray[1]['value']) {
			$('#validasi_modeling').html(`
											<small class="text-info">
												<i class="fa fa-info-circle"></i> Kuantitas data sampel harus sama
											</small>
										`);
		}
		else {
			$('#validasi_modeling').html(`
											<small class="text-info">
												<i class="fa fa-info-circle"></i> Silakan lakukan proses 'Pembagian Data' terlebih dahulu
											</small>
										`);
		}
		$('#validasi_modeling').removeClass('d-none');
	}
});

// AJAX - GET KOMPOSISI MODEL
$('#model-evaluasi').change(function() {

	$.ajax({
		url         : "/komposisi_model",
		data		: { 'model_name': $(this).val() },
		type        : "POST",
		dataType	: "json",
		success     : function(response) {
			$('#validasi_model_uji').addClass('d-none');

			var data = response.data[0];

			$('#komposisi-model').empty();
			$('#komposisi-model').html(`
				<input type="hidden" name="count_model" value="`+ data.sentiment_count +`" readonly />
				<em>Model</em> yang dipilih terdiri atas <span class="h6 text-dark">`+ data.sentiment_count +`</span> data:
				<p class="mb-0 ml-3"><span class="text-success">`+ data.sentiment_NONHS +`</span> Data bersentimen <span class="text-success">NONHS</span>, dan</p>
				<p class="mb-0 ml-3"><span class="text-danger">`+ data.sentiment_HS +`</span> Data bersentimen <span class="text-danger">HS</span>.</p>
			`);
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});

// AJAX - PENGUJIAN DATA
$('#uji_data').click(function() {

	var form_dataArray = $('form').serializeArray();
	var jumlah_data_tes = parseInt($('#jumlah_dataTes').html());

	// validasi data modeling
	$('#validasi_uji').addClass('d-none');
	$('#validasi_nilai_k').addClass('d-none');
	$('#validasi_nilai_k_2').addClass('d-none');
	$('#validasi_model_uji').addClass('d-none');
	if(jumlah_data_tes > 0 && form_dataArray.length == 3) {
		if(parseInt(form_dataArray[0]['value']) <= parseInt(form_dataArray[2]['value'])) {
			var content =	"";
		
			$.ajax({
				url         : "/evaluation",
				data		: $('form').serialize(),
				type        : "POST",
				dataType	: "json",
				beforeSend: function() {
					content +=	`	
									<br />
									<div class="modal-backdrop" style="background-color: rgba(0,0,0,0.3);"></div>
									<div class="loaderDiv my-5 m-auto"></div>
								`;
								
					$('#content_pengujian').html(content);
					$(".loaderDiv").show();
				},
				success     : function(response) {
					content +=	`
									<div class="table-responsive-sm">
										<table class="table table-bordered table-striped text-center" id="myTable">
											<thead>
												<tr>
													<th>No.</th>
													<th><em>Tweet</em></th>
													<th>Sentimen (Aktual)</th>
													<th>Sentimen (Prediksi)</th>
													<th>Tetangga Terdekat</th>
												</tr>
											</thead>
											<tbody>
								`;
					$.each(response.teks_database, function(index) {
						content +=	`
												<tr>
													<td>`+ ++index +`</td>
													<td class="text-left">`+ response.tweet_database[--index] +`</td>
													<td>`+ response.sentimen_database[index].toUpperCase() +`</td>
													<td><strong>`+ response.data_dict.label_prediction[index].toUpperCase() +`</strong> <small>(`+ response.data_dict.prob_prediction[index] +`%)</small></td>
													<td class="text-center">
														<button class="btn btn-outline-info" data-toggle="modal" data-target="#modalDetailTetangga`+ index +`"><i class="fa fa-search-plus"></i> Detail</button>

														<div class="modal fade" id="modalDetailTetangga`+ index +`" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
															<div class="modal-dialog modal-lg">
																<div class="modal-content">
																	<div class="modal-header">
																		<h5 class="modal-title" id="exampleModalLabel">Detail Tetangga Terdekat</h5>
																		<button type="button" class="close" data-dismiss="modal" aria-label="Close">
																		<span aria-hidden="true">&times;</span>
																		</button>
																	</div>
																	<div class="modal-body px-5">
																		<div class="container-fluid">
																			<h5 class="text-left">Data Uji</h5>
																			<table class="table table-bordered text-center">
																				<thead>
																					<tr class="bg-white">
																						<th>No.</th>
																						<th>Teks Bersih</th>
																						<th>Sentimen (Aktual)</th>
																						<th>Sentimen (Prediksi)</th>
																					</tr>
																				</thead>
																				<tbody>
																					<tr>
																						<td>1</td>
																						<td class="text-left">`+ response.teks_database[index] +`</td>
																						<td>`+ response.sentimen_database[index].toUpperCase() +`</td>
																						<td><strong>`+ response.data_dict.label_prediction[index].toUpperCase() +`</strong> <small>(`+ response.data_dict.prob_prediction[index] +`%)</small></td>
																					</tr>
																				</tbody>
																			</table>
																			<h5 class="text-left mt-4">Tetangga Terdekat (K=`+ response.data_dict.k +`)</h5>
																			<table class="table table-bordered table-striped text-center">
																				<thead>
																					<tr class="bg-white">
																						<th>No.</th>
																						<th>Teks Bersih</th>
																						<th>Sentimen Tetangga</th>
																						<th>Jarak Ketetanggaan</th>
																					</tr>
																				</thead>
																				<tbody>
									`;
															for(let j=0; j<response.data_dict.k; j++) {
																	content += 	`
																					<tr>
																						<td>`+ ++j +`</td>
																						<td class="text-left">`+ response.data_dict.teks_neighbors[index][--j] +`</td>
																						<td>`+ response.data_dict.sent_neighbors[index][j].toUpperCase() +`</td>
																						<td>`+ response.data_dict.near_neighbors[index][j] +`</td>
																					</tr>
																				`;
																					// <td>`+ Number((response.data_dict.near_neighbors[X][Y]).toFixed(5)); +`</td>
															}
					content +=		`											</tbody>
																			</table>
																		</div>
																	</div>
																</div>
															</div>
														</div>
													</td>
												</tr>
									`;
					});
					
					content +=	`			</tbody>
										</table>
									</div>
									<hr />
									<div class="row mt-4">
										<div class="col-md-6">
											<h5 class=" text-center"><em>Confusion Matrix</em></h5>
											<div class="d-flex justify-content-center container">
												<table class="table table-bordered text-center text-muted">
													<tbody>
														<tr>
															<td colspan="2" rowspan="2" style="border-top-color: white;	border-left-color: white;"></td>
															<td colspan="2" class="align-middle">Data Aktual</td>
														</tr>
														<tr>
															<td class="align-middle">Positive</td>
															<td class="align-middle">Negative</td>
														</tr>
														<tr>
															<td rowspan="2" class="align-middle p-0">Data Prediksi</td>
															<td class="align-middle">Positive</td>
															<td>
																<h5 class="mb-0 text-dark">`+ response.confusion_matrix['tp'] +`</h5>
																<small>TP (<em>True Positive</em>)</small>
															</td>
															<td>
																<h5 class="mb-0 text-dark">`+ response.confusion_matrix['fp'] +`</h5>
																<small>FP (<em>False Positive</em>)</small>
															</td>
														</tr>
														<tr>
															<td class="align-middle">Negative</td>
															<td>
																<h5 class="mb-0 text-dark">`+ response.confusion_matrix['fn'] +`</h5>
																<small>FN (<em>False Negative</em>)</small>
															</td>
															<td>
																<h5 class="mb-0 text-dark">`+ response.confusion_matrix['tn'] +`</h5>
																<small>TN (<em>True Negative</em>)</small>
															</td>
														</tr>
													</tbody>
												</table>
											</div>
										</div>
										<div class="col-md-6">
											<h5 class=" text-center">Detail Pengujian</h5>
											<div class="container text-muted">
												<table class="table table-borderless table-sm">
													<tbody>
														<tr>
															<td rowspan="4" class="text-right"><span class="h6">Akurasi</span></td>
															<td><span class="h6 text-muted">= ( TP + TN ) / ( TP + TN + FP + FN ) </span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= (`+ response.confusion_matrix['tp'] +` + `+ response.confusion_matrix['tn'] +`) / (`+ response.confusion_matrix['tp'] +` + `+ response.confusion_matrix['tn'] +` + `+ response.confusion_matrix['fp'] +` + `+ response.confusion_matrix['fn'] +`)</span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ (parseInt(response.confusion_matrix['tp']) + parseInt(response.confusion_matrix['tn'])) +` / `+ (parseInt(response.confusion_matrix['tp']) + parseInt(response.confusion_matrix['tn']) + parseInt(response.confusion_matrix['fp'])+ parseInt(response.confusion_matrix['fn'])) +` </span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['accuration'] +`</span>
															<i class="fa fa-arrow-right mx-3 text-muted"></i>
															<span class="h6 text-muted">`+ response.confusion_matrix['accuration'] +` x 100% =</span> <span class="h6">`+ Math.round(response.confusion_matrix['accuration'] * 100) +`%</span></td>
														</tr>
														<tr><td colspan="3"><hr/></td></tr>
														<tr>
															<td rowspan="4" class="text-right"><span class="h6">Presisi</span></td>
															<td><span class="h6 text-muted">= TP / ( TP + FP ) </span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['tp'] +` / (`+ response.confusion_matrix['tp'] +` + `+ response.confusion_matrix['fp'] +`)</span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['tp'] +` / `+ (parseInt(response.confusion_matrix['tp']) + parseInt(response.confusion_matrix['fp'])) +`</span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['precision'] +`</span>
															<i class="fa fa-arrow-right mx-3 text-muted"></i>
															<span class="h6 text-muted">`+ response.confusion_matrix['precision'] +` x 100% =</span> <span class="h6">`+ Math.round(response.confusion_matrix['precision'] * 100) +`%</span></td>
														</tr>
														<tr><td colspan="3"><hr/></td></tr>
														<tr>
															<td rowspan="4" class="text-right"><span class="h6"><em>Recall</em></span></td>
															<td><span class="h6 text-muted">= TP / ( TP + FN ) </span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['tp'] +` / (`+ response.confusion_matrix['tp'] +` + `+ response.confusion_matrix['fn'] +`)</span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['tp'] +` / `+ (parseInt(response.confusion_matrix['tp']) + parseInt(response.confusion_matrix['fn'])) +`</span></td>
														</tr>
														<tr>
															<td><span class="h6 text-muted">= `+ response.confusion_matrix['recall'] +`</span>
															<i class="fa fa-arrow-right mx-3 text-muted"></i>
															<span class="h6 text-muted">`+ response.confusion_matrix['recall'] +` x 100% =</span> <span class="h6">`+ Math.round(response.confusion_matrix['recall'] * 100) +`%</span></td>
														</tr>
													</tbody>
												</table>
											</div>
										</div>
									</div>
									<hr />
									<div class="container w-75 mt-3">
										<p class="text-center my-4">Hasil pengujian menggunakan algoritme <span class="h6">K-Nearest Neighbors (KNN)</span> dengan nilai <span class="h6">K=`+ response.data_dict.k +`</span>, didapatkan nilai akurasi sebesar  <span class="h6">`+ Math.round(response.confusion_matrix['accuration'] * 100) +`%</span>, nilai presisi sebesar <span class="h6">`+ (response.confusion_matrix['precision']* 100) +`%</span>, dan nilai <em>recall</em> sebesar <span class="h6">`+ (response.confusion_matrix['recall']* 100) +`%</span>.</p>
									</div>
									<div class="col-md-6 offset-md-3 col-sm-12 text-center">
										<a href="/evaluation" class="btn btn-info w-50 text-decoration-none"><i class="fa fa-arrow-left"></i> Kembali</a>
									</div>
								`;
					
					$('#content_pengujian').html(content);
					
					$(".loaderDiv").hide();
					$('#myTable').DataTable();
					
					$('body').removeClass('modal-open');
					$('.modal-backdrop').remove();
				},
				error     : function(x) {
					console.log(x.responseText);
				}
			});
		}
		else {
			$('#validasi_nilai_k_2').removeClass('d-none');
		}
	}
	else {
		if(jumlah_data_tes <= 0) {
			$('#validasi_uji').removeClass('d-none');
		}
		else if(form_dataArray == '') {
			$('#validasi_model_uji').removeClass('d-none');
			$('#validasi_nilai_k').removeClass('d-none');
		}
		else {
			if(form_dataArray[0]['name'] == 'nilai_k') {
				$('#validasi_model_uji').removeClass('d-none');
			}
			else {
				$('#validasi_nilai_k').removeClass('d-none');
			}
		}
	}
});

// AUTO REFRESH PAGE SETELAH PROSES PELABELAN AJAX
$('#modalLabeling').on('hidden.bs.modal', function () {
	window.location.href = "/labeling";
});


// TAMPIL TABEL DATA SLANGWORD [START]
var table_dataSlangword = $('#table_dataSlangword').DataTable({
	"deferRender": true,
	"ajax": "/list_slangword",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{ data: 'slangword' },
		{ data: 'kata_asli' },
		{
			data: null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		},
	],
});
// AKSI UPDATE DAN DELETE SLANGWORD DENGAN MODAL
$('#table_dataSlangword tbody').on( 'click', 'button', function () {
	var data = table_dataSlangword.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'update') {
		$("#slangwordEditModal").find("input[name='slangword']").val(data['slangword']);
		$("#slangwordEditModal").find("input[name='kata_asli']").val(data['kata_asli']);
		$("#slangwordEditModal").find("input[name='id']").val(data['id_slangword']);
		$('#slangwordEditModal').modal('show');
	}
	else if($(this).prop("value") == 'delete') {
		$("#slangwordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
		$("#slangwordDeleteModal").find("input[name='id']").val(data['id_slangword']);
		$('#slangwordDeleteModal').modal('show');
	}
});
// TAMPIL TABEL DATA SLANGWORD [END]


// TAMPIL TABEL DATA STOPWORD [START]
var table_dataStopword = $('#table_dataStopword').DataTable({
	"deferRender": true,
	"ajax": "/list_stopword",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{ data: 'stopword' },
		{
			data: null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		},
	],
});
// AKSI UPDATE DAN DELETE STOPWORD DENGAN MODAL
$('#table_dataStopword tbody').on( 'click', 'button', function () {
	var data = table_dataStopword.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'update') {
		$("#stopwordEditModal").find("input[name='stopword']").val(data['stopword']);
		$("#stopwordEditModal").find("input[name='id']").val(data['id_stopword']);
		$('#stopwordEditModal').modal('show');
	}
	else if($(this).prop("value") == 'delete') {
		$("#stopwordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
		$("#stopwordDeleteModal").find("input[name='id']").val(data['id_stopword']);
		$('#stopwordDeleteModal').modal('show');
	}
});
// TAMPIL TABEL DATA STOPWORD [END]


// TAMPIL DATA KATA NONHS [START]
var table_dataNONHSWord = $('#table_dataNONHSWord').DataTable({
	"deferRender": true,
	"ajax": "/list_positive_word",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{ data: 'positive_word' },
		{
			data: null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		},
	],
});
// AKSI UPDATE DAN DELETE KATA NONHS DENGAN MODAL
$('#table_dataNONHSWord tbody').on( 'click', 'button', function () {
	var data = table_dataNONHSWord.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'update') {
		$("#positive_wordEditModal").find("input[name='kata_NONHS']").val(data['positive_word']);
		$("#positive_wordEditModal").find("input[name='id']").val(data['id_NONHS']);
		$('#positive_wordEditModal').modal('show');
	}
	else if($(this).prop("value") == 'delete') {
		$("#positive_wordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
		$("#positive_wordDeleteModal").find("input[name='id']").val(data['id_NONHS']);
		$('#positive_wordDeleteModal').modal('show');
	}
});
// TAMPIL DATA KATA NONHS [END]


// TAMPIL DATA KATA HS [START]
var table_dataHSWord = $('#table_dataHSWord').DataTable({
	"deferRender": true,
	"ajax": "/list_negative_word",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{ data: 'negative_word' },
		{
			data: null,
			"defaultContent": `
				<button type="button" value="update" class="btn btn-warning mb-1"><i class="fa fa-pencil text-white"></i></button>
				<button type="button" value="delete" class="btn btn-danger mb-1"><i class="fa fa-trash"></i></button>								
			`
		},
	],
});
// AKSI UPDATE DAN DELETE KATA HS DENGAN MODAL
$('#table_dataHSWord tbody').on( 'click', 'button', function () {
	var data = table_dataHSWord.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'update') {
		$("#negative_wordEditModal").find("input[name='kata_HS']").val(data['negative_word']);
		$("#negative_wordEditModal").find("input[name='id']").val(data['id_HS']);
		$('#negative_wordEditModal').modal('show');
	}
	else if($(this).prop("value") == 'delete') {
		$("#negative_wordDeleteModal").find("p strong").html($(this).parents('tr').find('td').html());
		$("#negative_wordDeleteModal").find("input[name='id']").val(data['id_HS']);
		$('#negative_wordDeleteModal').modal('show');
	}
});
// TAMPIL DATA KATA HS [END]


// TAMPIL DATA CRAWLING [START]
$('#table_dataCrawling').DataTable({
	"deferRender": true,
	"ajax": "/list_data_crawling",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: 'text',
			className: 'text-left'
	 	},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
	],
});
// TAMPIL DATA CRAWLING [END]


// TAMPIL DATA PREPROCESSING [START]
var table_dataPreprocessing = $('#table_dataPreprocessing').DataTable({
	"deferRender": true,
	"ajax": "/list_data_preprocessing",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.clean_text +'<button type="button" value="modalTweetAsli" class="btn btn-info btn-sm float-right mt-2"><i class="fa fa-search"></i> Lihat Tweet Asli</button>'
			},
		},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
	],
});
// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataPreprocessing tbody').on( 'click', 'button', function () {
	var data = table_dataPreprocessing.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalTweetAsli') {
		$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
		$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
		$('#modalLihatTweetAsli').modal('show');
	}
});
// TAMPIL DATA PREPROCESSING [END]


// TAMPIL DATA LABELING (DENGAN LABEL) [START]
var table_dataWithLabel = $('#table_dataWithLabel').DataTable({
	"deferRender": true,
	"ajax": "/list_data_with_label",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.clean_text +'<button type="button" value="modalTweetAsli" class="btn btn-info btn-sm float-right mt-2"><i class="fa fa-search"></i> Lihat Tweet Asli</button>'
			},
		},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
		{
			data: null,
			"render": function (data, type, full, meta) {
				if(data.sentiment_type == 'NONHS') {
					return '<label class="btn btn-success disabled">NON HS</label>';
				}
				else if(data.sentiment_type == 'HS') {
					return '<label class="btn btn-danger disabled">HATESPEECH</label>';
				}
				return '<label class="btn btn-secondary disabled">NETRAL</label>';
			},
		},
	],
});
// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataWithLabel tbody').on( 'click', 'button', function () {
	var data = table_dataWithLabel.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalTweetAsli') {
		$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
		$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
		$('#modalLihatTweetAsli').modal('show');
	}
});
// TAMPIL DATA LABELING (DENGAN LABEL) [END]


// TAMPIL DATA LABELING (TANPA LABEL) [START]
var table_dataNoLabel = $('#table_dataNoLabel').DataTable({
	"deferRender": true,
	"ajax": "/list_data_no_label",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.text +'<button type="button" value="modalLihatCleanTextLabeling" class="btn btn-info btn-sm float-right mt-2"><i class="fa fa-search"></i> Lihat Teks Bersih</button>'
			},
		},
		{
			data: null,
			"render": function () {
				return `
					<select class="custom-select" name="label_data">
						<option value="" selected disabled>Pilih</option>
						<option value="NONHS">NONHS</option>
						<option value="HS">HS</option>
					</select>
				`;
			},
		},
	],
});
// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataNoLabel tbody').on( 'click', 'button', function () {
	var data = table_dataNoLabel.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalLihatCleanTextLabeling') {
		$("#modalLihatCleanTextLabeling").find("p[id='tweetAsliLabeling']").html(data['text']);
		$("#modalLihatCleanTextLabeling").find("p[id='tweetBersihLabeling']").html(data['clean_text']);
		$('#modalLihatCleanTextLabeling').modal('show');
		$('#modalLihatCleanTextLabeling').css('background-color', 'rgba(0,0,0,0.3)');
	}
});
// FUNGSI MENGEMBALIKAN TAMPILAN SETELAH NESTED MODAL modalLihatCleanTextLabeling DITUTUP
$('#modalLihatCleanTextLabeling').on('hidden.bs.modal', function () {
	$('body').addClass('modal-open');
});
// AJAX LABELING MANUAL
$('#table_dataNoLabel tbody').on( 'change', 'select[name="label_data"]', function () {
	var data = table_dataNoLabel.row($(this).parents('tr')).data();
	id = BigInt(data['id']).toString();
	value = $(this).find(":selected").text();
	
	$.ajax({
		url         : "/labeling",
		data		: {'id': id, 'value': value},
		type        : "POST",
		dataType	: "json",
		success     : function(response) {
			console.log(response);
		},
		error     : function(x) {
			console.log(x.responseText);
		}
	});
});
// TAMPIL DATA LABELING (TANPA LABEL) [END]


// TAMPIL DATA SPLIT (TRAINING) [START]
var table_dataTraining = $('#table_dataTraining').DataTable({
	"deferRender": true,
	"ajax": "/list_data_training",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.clean_text +'<button type="button" value="modalTweetAsli" class="btn btn-info btn-sm float-right mt-2"><i class="fa fa-search"></i> Lihat Tweet Asli</button>'
			},
		},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
		{
			data: null,
			"render": function (data, type, full, meta) {
				if(data.sentiment_type == 'NONHS') {
					return '<label class="btn btn-success disabled">NON HS</label>';
				}
				else if(data.sentiment_type == 'HS') {
					return '<label class="btn btn-danger disabled">HS</label>';
				}
				return '<label class="btn btn-secondary disabled">NETRAL</label>';
			},
		},
	],
});
// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataTraining tbody').on( 'click', 'button', function () {
	var data = table_dataTraining.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalTweetAsli') {
		$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
		$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
		$('#modalLihatTweetAsli').modal('show');
	}
});
// TAMPIL DATA SPLIT (TRAINING) [END]


// TAMPIL DATA SPLIT (TESTING) [START]
var table_dataTesting = $('#table_dataTesting').DataTable({
	"deferRender": true,
	"ajax": "/list_data_testing",
	"columns": [
		{
			data: null, 
			"render": function (data, type, full, meta) {
				return  meta.row + 1;
			}
		},
		{
			data: null,
			"render": function(data, type, full, meta) {
				return BigInt(data.id).toString();
			}
		},
		{
			data: null,
			className: 'text-left',
			"render": function (data, type, full, meta) {
				return data.clean_text +'<button type="button" value="modalTweetAsli" class="btn btn-info btn-sm float-right mt-2"><i class="fa fa-search"></i> Lihat Tweet Asli</button>'
			},
		},
		{ data: 'user' },
		{
			data: null,
			"render": function(data, type, full, meta) {
           		return moment(data.created_at).format("LLL");
			}
		},
		{
			data: null,
			"render": function (data, type, full, meta) {
				if(data.sentiment_type == 'NONHS') {
					return '<label class="btn btn-success disabled">NON HS</label>';
				}
				else if(data.sentiment_type == 'HS') {
					return '<label class="btn btn-danger disabled">HS</label>';
				}
				return '<label class="btn btn-secondary disabled">NETRAL</label>';
			},
		},
	],
});
// AKSI LIHAT TWEET ASLI DENGAN MODAL
$('#table_dataTesting tbody').on( 'click', 'button', function () {
	var data = table_dataTesting.row($(this).parents('tr')).data();
	if($(this).prop("value") == 'modalTweetAsli') {
		$("#modalLihatTweetAsli").find("p[id='tweetAsli']").html(data['text']);
		$("#modalLihatTweetAsli").find("p[id='tweetBersih']").html(data['clean_text']);
		$('#modalLihatTweetAsli').modal('show');
	}
});
// TAMPIL DATA SPLIT (TESTING) [END]
