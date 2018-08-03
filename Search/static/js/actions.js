/**
 * Created by camilojimenez on 19/05/17.
 */
var baseTablesVo = "http://localhost:8000/{% static 'tables' %}"
var aladin = A.aladin('#aladin-lite-div', {survey: "P/DSS2/color", fov:60,cooFrame:"0h8m05.63s +14d50m23.3s"});

var cat = A.catalog();
aladin.addCatalog(cat);

function addCataloog(catalUrl) {
    catalogInstance = A.catalogFromURL(baseTablesVo+"/"+catalUrl);
    aladin.addCatalog(catalogInstance);
}

function addToCatalog(source) {
    cat.addSources(A.source(source.ra, source.dec));
    aladin.gotoRaDec(source.ra, source.dec);
}

$(".selection-catalog").click(function () {
    var url = $(this).data("url");
    addCataloog(url);
});

$(".source-item").click(function () {
    var position = {}
    position.ra = $(this).data("ra");
    position.dec = $(this).data("dec");
    addToCatalog(position);
});