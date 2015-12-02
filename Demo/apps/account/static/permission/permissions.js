/* ViewModel */
var pageViewModel = null;
function PageViewModel(nowPage) {
	var viewModel = this;
	this._dummyObservable = ko.observable();
	this.nowPage = ko.observable(nowPage);
	this.newPermission = {
		username : ko.observable(null),
		password : ko.observable(null),
		repassword : ko.observable(null)
	}
}

/* Permissions */
$(function() {
	pageViewModel = new PageViewModel("帳號管理%>權限");
	ko.applyBindings(getMainViewModel());
	ko.applyBindings(pageViewModel, document.getElementById("_subPage"));
	getPermissions();
});

var datatable = null;
function getPermissions(){
	var pageSize = 10;
	var ajaxFun = function(sSource, aoData, fnCallback) {
		var url = _URLS['permission_getPermissions']

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
						modelresult.push(new Permission(result.result[i]));
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

	datatable = $('#userList').DataTable(
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
					"title" : "CODENAME",
					"data" : "codename",
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
					"title" : "NAME",
					"data" : "name",
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
					"title" : "",
					"data" : "date_joined",
					"render" : function(data, type, full, meta) {
						var html = "";
						html += '<button type="button" class="btn btn-xs btn-danger" onClick="deleteUser(\''+full.username+'\')"><i class="fa fa-fw fa-remove"></i></button>'
						return html;
					},
					"width" : "10%",
					"className" : "text-center"
				}

			],
			"fnServerData" : ajaxFun
		});
	$('#userList tbody').on('mouseover', 'tr', function () {
		var data = datatable.row(this).data();
	} );
}

function deleteUser(username){
	var fun =  function() {
		$.ajax({
			url: _URLS['account_deleteUser'].replace("(?P&lt;username&gt;\w+)", username),
			type: 'POST',
			data: {username: username},
			success: function (result) {
				displayMessageDialog("刪除成功");
				datatable.ajax.reload();
			}
		});
	}
	displayConfirmDialog("確認刪除？", fun);
}

function bindSimpleUserCreate(){

	var formData = new FormData();
	formData.append('username', pageViewModel.newUser.username());
	formData.append('password', pageViewModel.newUser.password());
	if($("#profile_image")[0].files.length != 0)
		formData.append('file', $("#profile_image")[0].files[0]);

	var fun = function(){
		$.ajax({
			url: _URLS['account_newUser'],
			type: 'POST',
			data: formData,
			async: false,
			success: function (data) {
				if(data.success){
					clearSimpleUserCreate();
					datatable.ajax.reload();
				}else{

				}
			},
			cache: false,
			contentType: false,
			processData: false
		});
	}
	displayConfirmDialog("確認新增？", fun);
}

function clearSimpleUserCreate(){
	pageViewModel.newUser.username(null);
	pageViewModel.newUser.password(null);
	pageViewModel.newUser.repassword(null);
	$("#profile_image").val(null)
}

function getWhoAmI(username){
	var url = _URLS['account_whoAmI'];
	if(username != null){
		url = _URLS['account_getUser'].replace("(?P&lt;username&gt;\w+)", username)
	}

	$.ajax({
		type : 'GET',
		url : url,
		contentType : 'application/json',
		success : function(result) {
			pageViewModel.userProfile.username(result.user.username);
			pageViewModel.userProfile.email(result.user.email);
			pageViewModel.userProfile.profile_image(result.profile_image);
			pageViewModel._dummyObservable.notifySubscribers();
		},
		error : function(result) {
			alert("取得Profile失敗。");
		}
	});
}