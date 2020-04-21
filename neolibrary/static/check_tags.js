$(document).ready(function(){
    $("#select_tags").click(function(){
        $("div.form-check").each(function() {
            var cb = $(this).find("input.form-check-input");
            var count = $(this).find("span.float-right").text().replace(/ /g,'');
            
            if(count == 0)
                cb.prop('checked', !cb.prop('checked'));
        });
    });
});
