/* ViewModel */
var pageViewModel = null;
function PageViewModel(nowPage) {
    var viewModel = this;
    this._dummyObservable = ko.observable();
    this.nowPage = ko.observable(nowPage);
    this.newUser = {
        username: ko.observable(null),
        password: ko.observable(null),
        repassword: ko.observable(null)
    }
    this.userProfile = {
        username: ko.observable(null),
        email: ko.observable(null),
        profile_image: ko.observable(null),
        groups: ko.observableArray([]),
        selectGroups: [],
        permissions: ko.observableArray([]),
        selectPermissions: []
    }
    this.profileImage = ko.pureComputed(function () {
        pageViewModel._dummyObservable();
        return _URLS['account_getProfileImage'] + "?path=" + this.userProfile.profile_image();
    }, this);

}

function bindingHandlers() {
}

/* Accounts */
$(function () {
    pageViewModel = new PageViewModel("帳號管理%>使用者");
    bindingHandlers();
    ko.applyBindings(getMainViewModel());
    ko.applyBindings(pageViewModel, document.getElementById("_subPage"));
    getUsers();
    getWhoAmI();
    getGroups();
    getPermissions();

    $("#groupList").select2(
        {
            placeholder: "請選擇群組",
            allowClear: true,
            width: '100%'
        }
    );
    $("#permissionList").select2(
        {
            placeholder: "請選擇權限",
            allowClear: true,
            width: '100%'
        }
    );
});

var datatable = null;
function getUsers() {
    var pageSize = 10;
    var ajaxFun = function (sSource, aoData, fnCallback) {
        var url = _URLS['account_getUsers']

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
                        modelresult.push(new User(result.result[i].user));
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

    datatable = $('#userList').DataTable(
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
                    "width": "15%",
                    "className": "text-center"
                },
                {
                    "targets": 1,
                    "searchable": false,
                    "orderable": false,
                    "title": "EMAIL",
                    "data": "email",
                    "render": function (data, type, full, meta) {
                        return data;
                    },
                    "width": "30%",
                    "className": "text-center"
                },
                {
                    "targets": 2,
                    "searchable": false,
                    "orderable": false,
                    "title": "LAST LOGIN",
                    "data": "last_login",
                    "render": function (data, type, full, meta) {
                        return data != null ? moment(data).format('YYYY-MM-DD HH:mm:ss') : "";
                    },
                    "width": "20%",
                    "className": "text-center"
                },
                {
                    "targets": 3,
                    "searchable": false,
                    "orderable": false,
                    "title": "DATE JOINED",
                    "data": "date_joined",
                    "render": function (data, type, full, meta) {
                        return data != null ? moment(data).format('YYYY-MM-DD') : "";
                    },
                    "width": "20%",
                    "className": "text-center"
                },
                {
                    "targets": 4,
                    "searchable": false,
                    "orderable": false,
                    "title": "",
                    "data": "date_joined",
                    "render": function (data, type, full, meta) {
                        var html = "";
                        html += '<button type="button" class="btn btn-xs btn-danger" onClick="deleteUser(\'' + full.username + '\')"><i class="fa fa-fw fa-remove"></i></button>'
                        return html;
                    },
                    "width": "10%",
                    "className": "text-center"
                }

            ],
            "fnServerData": ajaxFun
        });
    $('#userList tbody').on('mouseover', 'tr', function () {
        var data = datatable.row(this).data();
        getWhoAmI(data.username);
    });
}

function deleteUser(username) {
    var fun = function () {
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

function bindSimpleUserCreate() {

    var formData = new FormData();
    formData.append('username', pageViewModel.newUser.username());
    var password = CryptoJS.MD5(pageViewModel.newUser.password());
    formData.append('password', password);
    if ($("#profile_image")[0].files.length != 0)
        formData.append('file', $("#profile_image")[0].files[0]);

    var fun = function () {
        $.ajax({
            url: _URLS['account_newUser'],
            type: 'POST',
            data: formData,
            async: false,
            success: function (data) {
                if (data.success) {
                    clearSimpleUserCreate();
                    datatable.ajax.reload();
                } else {

                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
    }
    displayConfirmDialog("確認新增？", fun);
}

function clearSimpleUserCreate() {
    pageViewModel.newUser.username(null);
    pageViewModel.newUser.password(null);
    pageViewModel.newUser.repassword(null);
    $("#profile_image").val(null)
}

function getWhoAmI(username) {
    var url = _URLS['account_whoAmI'];
    if (username != null) {
        url = _URLS['account_getUser'].replace("(?P&lt;username&gt;\w+)", username)
    }

    $.ajax({
        type: 'GET',
        url: url,
        contentType: 'application/json',
        success: function (result) {
            pageViewModel.userProfile.username(result.user.username);
            pageViewModel.userProfile.email(result.user.email);
            pageViewModel.userProfile.profile_image(result.profile_image);

            groups = [];
            result.user.groups.forEach(function(item){
                groups[groups.length] = item.name;
            });
            pageViewModel.userProfile.selectGroups = groups;
            $("#groupList").select2("val", groups);

            permissions = [];
            result.user.user_permissions.forEach(function(item){
                permissions[permissions.length] = item.codename;
            });
            pageViewModel.userProfile.selectPermissions = permissions;
            $("#permissionList").select2("val", permissions);

            pageViewModel._dummyObservable.notifySubscribers();

        },
        error: function (result) {
            alert("取得Profile失敗。");
        }
    });
}

function getGroups() {
    $.ajax({
        type: 'GET',
        url: _URLS['group_getGroups']+"?size=10000",
        contentType: 'application/json',
        success: function (result) {
            pageViewModel.userProfile.groups(result.result);
        },
        error: function (result) {
            alert("取得Group失敗。");
        }
    });
}

function getPermissions() {
    $.ajax({
        type: 'GET',
        url: _URLS['permission_getPermissions']+"?size=10000",
        contentType: 'application/json',
        success: function (result) {
            pageViewModel.userProfile.permissions(result.result);
        },
        error: function (result) {
            alert("取得Permission失敗。");
        }
    });
}

function saveUser(){

    var formData = new FormData();
    pageViewModel.userProfile.selectGroups.forEach(function(item){
        formData.append('groups', item);
    });
    //formData.append('groups', pageViewModel.userProfile.selectGroups);
    pageViewModel.userProfile.selectPermissions.forEach(function(item){
        formData.append('user_permissions', item);
    });
    //formData.append('user_permissions', pageViewModel.userProfile.selectPermissions);

    var fun = function () {
        $.ajax({
            url: _URLS['account_editUser'].replace("(?P&lt;username&gt;\w+)", pageViewModel.userProfile.username()),
            type: 'POST',
            data: formData,
            async: false,
            success: function (data) {
                if (data.success) {
                    displayMessageDialog("修改成功");
                } else {

                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
    }
    displayConfirmDialog("確認修改？", fun);
}