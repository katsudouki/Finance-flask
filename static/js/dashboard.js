$(document).ready(function(){
    $('.panel li').click(function(){
        $('.panel li').removeClass('panelclicked');
        $(this).addClass('panelclicked');
        var id = $(this).attr('id'); // Obtém o ID do <li> clicado
        $('#main').load(id);
    });
});

