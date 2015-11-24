/*
    ajax 處理
 */
$(function() {
	/*$(document).ajaxError(function(event, jqxhr, settings, thrownError) {
		// 登入失效
		if (jqxhr.status == 403) {
			displayMessageDialog("登入逾時，請重新登入。", function(){location.href = SERVICE_URL["root"] + "/login";});
		}
	});
	$(document).ajaxSuccess(function(event, jqxhr, settings, thrownSuccess) {
		// console.log( "Triggered ajaxSuccess handler." );
	});*/
});

/*
    main viewmodel
 */
function MainViewModel(menu) {
	this.menuData = ko.observableArray(menu);
	this.nowPageNameLevelOne = ko.computed(function() {
		return getNowPageNameLevelOne();
	}, this);
	this.nowPageNameLevelTwo = ko.computed(function() {
		return getNowPageNameLevelTwo();
	}, this);
	this.nowPageIcon = ko.computed(function() {
		return getNowPageIcon();
	}, this);
	this.pageRoute = ko.observableArray(getNowPageRoute());
}

/*
    model
 */
function badge(text, color) {
	this.text = text;
	this.color = color;
}

function subMenu(text, url, active) {
	this.text = text;
	this.active = active;
	this.url = url;
}

function singleMenu(text, icon, url, badge, subMenuList, active) {
	this.text = text;
	this.icon = icon;
	this.url = url;
	this.badge = badge;
	this.active = active;
	this.subMenuList = subMenuList;
}