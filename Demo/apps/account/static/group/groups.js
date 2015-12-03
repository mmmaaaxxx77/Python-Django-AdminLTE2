/* ViewModel */
var pageViewModel = null;
function PageViewModel(nowPage) {
    var viewModel = this;
    this._dummyObservable = ko.observable();
    this.nowPage = ko.observable(nowPage);
    this.nowSelectedGroup = null;
    this.showNowSelectedGroup = ko.pureComputed(function () {
        pageViewModel._dummyObservable();
        if (this.nowSelectedGroup != null)
            return " - " + this.nowSelectedGroup.name;
        else
            return null;
    }, this);
    this.newGroup = {
		name : ko.observable(null)
	}
}

/* Groups */
$(function () {
    pageViewModel = new PageViewModel("帳號管理%>群組");
    ko.applyBindings(getMainViewModel());
    ko.applyBindings(pageViewModel, document.getElementById("_subPage"));
    getGroups();
    getGroupUsers();
});

var datatable = null;
function getGroups() {
    var pageSize = 10;
    var ajaxFun = function (sSource, aoData, fnCallback) {
        var url = _URLS['group_getGroups']

        var startO = null;
        var lengthO = null;
        var drawO = null;
        aoData.forEach(function (item) {
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

        var page = Math.floor(startO.value / lengthO.value);
        page++;

        $.ajax({
            type: 'GET',
            url: url + "?page=" + page + "&size=" + pageSize,
            contentType: 'application/json',
            success: function (result) {
                if (result.success) {
                    var modelresult = [];
                    for (var i = 0; i < result.result.length; i++) {
                        modelresult.push(new Group(result.result[i]));
                    }
                    var dat = {
                        draw: drawO.value,
                        data: modelresult,
                        recordsTotal: result.totalResults,
                        recordsFiltered: result.totalResults
                    }
                    fnCallback(dat);
                } else {
                    alert("取得列表失敗。");
                    var dat = {
                        draw: drawO.value,
                        data: [],
                        recordsTotal: 0,
                        recordsFiltered: 0
                    }
                    fnCallback(dat);
                }
            },
            error: function (result) {
                alert("取得列表失敗。");
                var dat = {
                    draw: drawO.value,
                    data: [],
                    recordsTotal: 0,
                    recordsFiltered: 0
                }
                fnCallback(dat);
            }
        });
    }

    datatable = $('#groupList').DataTable(
        {
            "bProcessing": true,
            "pageLength": pageSize,
            "bServerSide": true,
            "bFilter": false,
            "bLengthChange": false,
            "columnDefs": [
                {
                    "targets": 0,
                    "searchable": false,
                    "orderable": false,
                    "title": "NAME",
                    "data": "name",
                    "render": function (data, type, full, meta) {
                        return data;
                    },
                    "width": "80%",
                    "className": "text-center"
                },
                {
                    "targets": 1,
                    "searchable": false,
                    "orderable": false,
                    "title": "",
                    "data": "name",
                    "render": function (data, type, full, meta) {
                        var html = "";
						html += '<button type="button" class="btn btn-xs btn-danger" onClick="deleteGroup(\''+full.name+'\')"><i class="fa fa-fw fa-remove"></i></button>'
                        return html;
                    },
                    "width": "20%",
                    "className": "text-center"
                }

            ],
            "fnServerData": ajaxFun
        });
    $('#groupList tbody').on('mouseover', 'tr', function () {
        var data = datatable.row(this).data();
        pageViewModel.nowSelectedGroup = data;
        pageViewModel._dummyObservable.notifySubscribers();
        userdatatable.ajax.reload();
    });
}

var userdatatable = null;
function getGroupUsers() {
    var pageSize = 10;
    var ajaxFun = function (sSource, aoData, fnCallback) {
        var name = "";
        var url = _URLS['group_getGroupUsers'];
        if (pageViewModel.nowSelectedGroup != null) {
            name = pageViewModel.nowSelectedGroup.name;
            url = _URLS['group_getGroupUsers'].replace("(?P&lt;name&gt;\w+)", name)
        }

        var startO = null;
        var lengthO = null;
        var drawO = null;
        aoData.forEach(function (item) {
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

        var page = Math.floor(startO.value / lengthO.value);
        page++;

        if (pageViewModel.nowSelectedGroup != null) {
            $.ajax({
                type: 'GET',
                url: url + "?page=" + page + "&size=" + pageSize,
                contentType: 'application/json',
                success: function (result) {
                    if (result.success) {
                        var modelresult = [];
                        for (var i = 0; i < result.result.length; i++) {
                            modelresult.push(new User(result.result[i]));
                        }
                        var dat = {
                            draw: drawO.value,
                            data: modelresult,
                            recordsTotal: result.totalResults,
                            recordsFiltered: result.totalResults
                        }
                        fnCallback(dat);
                    } else {
                        alert("取得列表失敗。");
                        var dat = {
                            draw: drawO.value,
                            data: [],
                            recordsTotal: 0,
                            recordsFiltered: 0
                        }
                        fnCallback(dat);
                    }
                },
                error: function (result) {
                    alert("取得列表失敗。");
                    var dat = {
                        draw: drawO.value,
                        data: [],
                        recordsTotal: 0,
                        recordsFiltered: 0
                    }
                    fnCallback(dat);
                }
            });
        } else {
            var dat = {
                draw: drawO.value,
                data: [],
                recordsTotal: 0,
                recordsFiltered: 0
            }
            fnCallback(dat);
        }
    }

    userdatatable = $('#groupUsersList').DataTable(
        {
            "bProcessing": true,
            "pageLength": pageSize,
            "bServerSide": true,
            "bFilter": false,
            "bLengthChange": false,
            "pagingType": "simple",
            "columnDefs": [
                {
                    "targets": 0,
                    "searchable": false,
                    "orderable": false,
                    "title": "USERNAME",
                    "data": "username",
                    "render": function (data, type, full, meta) {
                        return data;
                    },
                    "width": "80%",
                    "className": "text-center"
                },
                {
                    "targets": 1,
                    "searchable": false,
                    "orderable": false,
                    "title": "",
                    "data": "username",
                    "render": function (data, type, full, meta) {
                        var html = "";
						html += '<button type="button" class="btn btn-xs btn-danger" onClick="deleteUserGroup(\''+full.username+'\')"><i class="fa fa-fw fa-remove"></i></button>'
						return html;
                    },
                    "width": "20%",
                    "className": "text-center"
                }

            ],
            "fnServerData": ajaxFun
        });
    $('#groupUsersList tbody').on('mouseover', 'tr', function () {
        var data = datatable.row(this).data();
    });
}

function createGroup(){

	var formData = new FormData();
	formData.append('name', pageViewModel.newGroup.name());

	var fun = function(){
		$.ajax({
			url: _URLS['group_newGroup'],
			type: 'POST',
			data: formData,
			async: false,
			success: function (data) {
				if(data.success){
					clearSimpleGroupCreate();
					datatable.ajax.reload();
                    displayMessageDialog("新增成功");
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

function clearSimpleGroupCreate(){
    pageViewModel.newGroup.name(null);
}

function deleteGroup(name){
	var fun =  function() {
		$.ajax({
			url: _URLS['group_deleteGroup'].replace("(?P&lt;name&gt;\w+)", name),
			type: 'POST',
			data: {},
			success: function (result) {
                if(result.success) {
                    datatable.ajax.reload();
                    displayMessageDialog("刪除成功");
                }else{
                    displayMessageDialog("刪除失敗：" + result.result);
                }
			},
            error: function (result){
                displayMessageDialog("刪除失敗：" + result.result);
            }
		});
	}
	displayConfirmDialog("確認刪除？", fun);
}

function deleteUserGroup(username){
    var name = pageViewModel.nowSelectedGroup.name;
	var fun =  function() {
		$.ajax({
			url: _URLS['group_deleteUserGroup'].replace("(?P&lt;username&gt;\w+)", username).replace("(?P&lt;name&gt;\w+)", name),
			type: 'POST',
			data: {},
			success: function (result) {
                if(result.success) {
                    userdatatable.ajax.reload();
                    displayMessageDialog("刪除成功");
                }else{
                    displayMessageDialog("刪除失敗：" + result.result);
                }
			},
            error: function (result){
                displayMessageDialog("刪除失敗：" + result.result);
            }
		});
	}
	displayConfirmDialog("確認刪除？", fun);
}