var clear_fields = function(){
    var objectID = $("#data_structure_id").html();
    $.ajax({
        url : clearFieldsUrl,
        type : "POST",
        data:{
            'id': objectID
        },
        dataType: "json",
        success: function(data){
            $("#xsd_form").html(data.xsdForm);
        }
    });
};

$('.btn.clear-fields').on('click', clear_fields);
