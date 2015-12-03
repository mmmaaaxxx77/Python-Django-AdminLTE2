/* ViewModel */
var pageViewModel = null;
function PageViewModel(nowPage) {
    var viewModel = this;
    this._dummyObservable = ko.observable();
    this.nowPage = ko.observable(nowPage);
    this.nowSelectedPermission = null;
    this.showNowSelectedPermission = ko.pureComputed(function () {
        pageViewModel._dummyObservable();
        if (this.nowSelectedPermission != null)
            return " - " + this.nowSelectedPermission.codename;
        else
            return null;
    }, this);
}

/* Permissions */
$(function () {
    pageViewModel = new PageViewModel("帳號管理%>權限");
    ko.applyBindings(getMainViewModel());
    ko.applyBindings(pageViewModel, document.getElementById("_subPage"));
    getPermissions();
    getPermissionUsers();
});

var datatable = null;
function getPermissions() {
    var pageSize = 10;
    var ajaxFun = function (sSource, aoData, fnCallback) {
        var url = _URLS['permission_getPermissions']

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
                        modelresult.push(new Permission(result.result[i]));
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

    datatable = $('#permissionList').DataTable(
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
                    "title": "CODENAME",
                    "data": "codename",
                    "render": function (data, type, full, meta) {
                        return data;
                    },
                    "width": "40%",
                    "className": "text-center"
                },
                {
                    "targets": 1,
                    "searchable": false,
                    "orderable": false,
                    "title": "NAME",
                    "data": "name",
                    "render": function (data, type, full, meta) {
                        return data;
                    },
                    "width": "60%",
                    "className": "text-center"
                }

            ],
            "fnServerData": ajaxFun
        });
    $('#permissionList tbody').on('mouseover', 'tr', function () {
        var data = datatable.row(this).data();
        pageViewModel.nowSelectedPermission = data;
        pageViewModel._dummyObservable.notifySubscribers();
        userdatatable.ajax.reload();
    });
}

var userdatatable = null;
function getPermissionUsers() {
    var pageSize = 10;
    var ajaxFun = function (sSource, aoData, fnCallback) {
        var codename = "";
        var url = _URLS['permission_getPermissionUsers'];
        if (pageViewModel.nowSelectedPermission != null) {
            codename = pageViewModel.nowSelectedPermission.codename;
            url = _URLS['permission_getPermissionUsers'].replace("(?P&lt;codename&gt;\w+)", codename)
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

        if (pageViewModel.nowSelectedPermission != null) {
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

    userdatatable = $('#permissionUsersList').DataTable(
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
						html += '<button type="button" class="btn btn-xs btn-danger" onClick="deleteUserPermission(\''+full.username+'\')"><i class="fa fa-fw fa-remove"></i></button>'
						return html;
                    },
                    "width": "20%",
                    "className": "text-center"
                }

            ],
            "fnServerData": ajaxFun
        });
    $('#permissionUsersList tbody').on('mouseover', 'tr', function () {
        var data = datatable.row(this).data();
    });
}

function deleteUserPermission(username){
    var codename = pageViewModel.nowSelectedPermission.codename;
	var fun =  function() {
		$.ajax({
			url: _URLS['permission_deleteUserPermission'].replace("(?P&lt;username&gt;\w+)", username).replace("(?P&lt;codename&gt;\w+)", codename),
			type: 'POST',
			data: {},
			success: function (result) {
				displayMessageDialog("刪除成功");
			}
		});
	}
	displayConfirmDialog("確認刪除？", fun);
}