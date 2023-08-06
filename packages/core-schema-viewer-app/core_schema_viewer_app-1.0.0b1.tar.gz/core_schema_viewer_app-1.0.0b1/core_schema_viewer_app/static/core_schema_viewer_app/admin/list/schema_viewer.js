/**
 * on Mouseup and Keyup of default checkbox
 * uncheck all other default checkbox minus the source
 * enable the paired visibility checkbox
 */
var onCheckboxDefaultMouseupAndKeyup = function(event){
    event.preventDefault();
    source = this;
    $(".table-schema-viewer-template input:checked").filter("[class='chk-is-default']").each(function() {
        if (source != this){
            this.checked = false;
        }
        $(this).closest("tr").find(".chk-is-visible").prop("disabled", false);
    });
}

/**
 * on Changes of default checkbox
 * disable to avoid clicking
 * toggle the template
 */
var onCheckboxDefaultChanged = function(event){
    $(this).prop("disabled", true);
    template_schema_id = $(this).closest("tr").data().templateSchemaViewerId;
    toggleTemplateSchemaDefault(this, template_schema_id);
}

/**
 * toggle the template to default
 * disable and check the paired visibility checkbox if default = true
 */
var toggleTemplateSchemaDefault = function(source, template_schema_id){
    $.ajax({
        url : setTemplateSchemaDefaultUrl,
        type : "POST",
        data: {
            template_schema_id,
        },
        success: function(data){
            $(source).prop("disabled", false);
            is_visible_checkbox = $(source).closest("tr").find(".chk-is-visible");
            if(source.checked){
                $(is_visible_checkbox).prop("checked", true);
                $(is_visible_checkbox).prop("disabled", true);
            }
        }
    });
}

/**
 * on change of 'visible' checkbox
 * disable to avoid clicking
 * toggle the visibility
 */
var onCheckboxVisibleChanged = function(event){
    $(this).prop("disabled", true);
    template_schema_id = $(this).closest("tr").data().templateSchemaViewerId;
    toggleTemplateSchemaVisibility(this, template_schema_id);
}

/**
 * toggle the template visibility
 */
var toggleTemplateSchemaVisibility = function(source, template_schema_id){
    $.ajax({
        url : toggleTemplateSchemaVisibilityUrl,
        type : "POST",
        data: {
            template_schema_id,
        },
        success: function(data){
            $(source).prop("disabled", false);
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to checkbox (visible)
    $(".chk-is-visible").on("change", onCheckboxVisibleChanged);
    // bind change event to checkbox (default)
    $(".chk-is-default").on("change", onCheckboxDefaultChanged);
    // bind mouseup keyup event to checkbox (default) (called before change)
    $(".chk-is-default").on("mouseup keyup", onCheckboxDefaultMouseupAndKeyup);
});
