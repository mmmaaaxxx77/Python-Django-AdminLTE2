/* ViewModel */
var pageViewModel = null;
function PageViewModel(nowPage) {
	this.nowPage = ko.observable(nowPage);
	this.newUser = {
		username : ko.observable(null),
		password : ko.observable(null),
		repassword : ko.observable(null)
	}
}

/* Accounts */
$(function() {
	pageViewModel = new PageViewModel("帳號管理%>使用者");
	ko.applyBindings(getMainViewModel());
	ko.applyBindings(pageViewModel, document.getElementById("_subPage"));
	getUsers();
});

var datatable = null;
function getUsers(){
	var pageSize = 10;
	var ajaxFun = function(sSource, aoData, fnCallback) {
		var url = _URLS['account_getUsers']

		var startO = null;
		var lengthO = null;
		var drawO = null;
		aoData.forEach(function(item) {
			if (item.name == "start") {
				startO = item;
			}
			if (item.name == "length") {
				lengthO = item;
			}
			if (item.name == "draw") {
				drawO = item;
			}
		});

		var page = Math.floor(startO.value/lengthO.value);
		page++;

		$.ajax({
			type : 'GET',
			url : url + "?page=" + page + "&size=" + pageSize,
			contentType : 'application/json',
			success : function(result) {
				if (result.success) {
					var modelresult = [];
					for(var i = 0 ; i < result.result.length ; i++){
						modelresult.push(new User(result.result[i]));
					}
					var dat = {
						draw : drawO.value,
						data : modelresult,
						recordsTotal : result.totalResults,
						recordsFiltered : result.totalResults
					}
					fnCallback(dat);
				} else {
					alert("取得列表失敗。");
					var dat = {
						draw : drawO.value,
						data : [],
						recordsTotal : 0,
						recordsFiltered : 0
					}
					fnCallback(dat);
				}
			},
			error : function(result) {
				alert("取得列表失敗。");
				var dat = {
					draw : drawO.value,
					data : [],
					recordsTotal : 0,
					recordsFiltered : 0
				}
				fnCallback(dat);
			}
		});
	}

	datatable = $('#ideaList').DataTable(
		{
			"bProcessing" : true,
			"pageLength" : pageSize,
			"bServerSide" : true,
			"bFilter" : false,
			"bLengthChange" : false,
			"columnDefs" : [
				{
					"targets": 0,
					"searchable" : false,
					"orderable" : false,
					"title" : "USERNAME",
					"data" : "username",
					"render" : function(data, type, full, meta) {
						return data;
					},
					"width" : "15%",
					"className" : "text-center"
				},
				{
					"targets": 1,
					"searchable" : false,
					"orderable" : false,
					"title" : "EMAIL",
					"data" : "email",
					"render" : function(data, type, full, meta) {
						return data;
					},
					"width" : "30%",
					"className" : "text-center"
				},
				{
					"targets": 2,
					"searchable" : false,
					"orderable" : false,
					"title" : "LAST LOGIN",
					"data" : "last_login",
					"render" : function(data, type, full, meta) {
						return data!=null?moment(data).format('YYYY-MM-DD HH:mm:ss'):"";
					},
					"width" : "20%",
					"className" : "text-center"
				},
				{
					"targets": 3,
					"searchable" : false,
					"orderable" : false,
					"title" : "DATE JOINED",
					"data" : "date_joined",
					"render" : function(data, type, full, meta) {
						return data!=null?moment(data).format('YYYY-MM-DD'):"";
					},
					"width" : "20%",
					"className" : "text-center"
				},
				{
					"targets": 4,
					"searchable" : false,
					"orderable" : false,
					"title" : "",
					"data" : "date_joined",
					"render" : function(data, type, full, meta) {
						return "";
					},
					"width" : "10%",
					"className" : "text-center"
				}

			],
			"fnServerData" : ajaxFun
		});
}

function addUser(){
	$.ajax({
		url: _URLS['account_editUser'],
		type: 'POST',
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify({username:"test22", password:"test22"}),
		success: function(result) {
			alert(result);
		}
	});
}

function bindSimpleUserCreate(){

		var formData = new FormData();
		formData.append('username', pageViewModel.newUser.username());
		formData.append('password', pageViewModel.newUser.password());
		if($("#profile_image")[0].files.length != 0)
			formData.append('file', $("#profile_image")[0].files[0]);

		$.ajax({
			url: _URLS['account_editUser'],
			type: 'POST',
			data: formData,
			async: false,
			success: function (data) {
				alert(data)
			},
			cache: false,
			contentType: false,
			processData: false
		});
}