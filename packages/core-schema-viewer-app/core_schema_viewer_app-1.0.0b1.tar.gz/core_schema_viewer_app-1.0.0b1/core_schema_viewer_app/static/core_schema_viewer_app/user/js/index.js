/**
 * Destinations views enumeration
 */
var DestinationViews = {
    TabbedView: "tabbed",
    OxygenView: "oxygen",
    SandboxView: "sandbox",
};

/**
 * on click of schema view tabbed button
 */
var onButtonClick = function(event){
    template_id = $("#id_schema").val();
    if(template_id) {
        redirectToView(template_id, event.data.destination_view);
    }
}

/**
 * on click of download button
 */
var onButtonDownloadClick = function(event){
    template_id = $("#id_schema").val();
    if(template_id) {
        downloadTemplate(template_id);
    }
}

/**
 * download the template
 */
var downloadTemplate = function(template_id){
    $(location).attr('href', downloadTemplateUrl + "?template_id=" + template_id);
}

/**
 * redirect to schemaViewTabbed
 */
var redirectToView = function(template_id, destination) {
    var url = redirectUrl
                + "?template_id="
                + template_id
                + "&destination_view="
                + destination
    window.open(url, '_blank');
}

// .ready() called.
$(function() {
    // bind change event to checkbox (visible)
    $(".btn-download-template").on("click", onButtonDownloadClick);
    $("#schema_view").on("click", {destination_view: DestinationViews.TabbedView}, onButtonClick);
    $("#oxygen-viewer").on("click", {destination_view: DestinationViews.OxygenView}, onButtonClick);
    $("#sandbox_view").on("click", {destination_view: DestinationViews.SandboxView}, onButtonClick);
});