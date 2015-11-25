/* ViewModel */
var pageViewModel = null;
function PageViewModel(nowPage) {
	this.nowPage = ko.observable(nowPage);
}

/* Accounts */
$(function() {
	pageViewModel = new PageViewModel("帳號管理");
    ko.applyBindings(getMainViewModel());
	ko.applyBindings(pageViewModel, document.getElementById("_subPage"));
});