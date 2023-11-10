function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}


function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    return false;
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    console.log(total)
    if (total > 1){
        btn.closest('.add-participant-form').remove();
        var forms = $('.add-participant-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

$(document).on('click', '.add-participant', function(e){
    e.preventDefault();
    cloneMore('.add-participant-form:last', 'add-participant');
    return false;
});

$(document).on('click', '.remove-participant', function(e){
    e.preventDefault();
    deleteForm('add-participant', $(this));
    return false;
});


$('input[name="application_type"]').on('click', function (e) {
    if ($(this).val() == 'IN'){
        $('#id_team_name').prop("required", false).val("");
        $('.row.team_name').hide();
    } else {
        $('#id_team_name').prop("required", true);
        $('.row.team_name').show();
    }
});