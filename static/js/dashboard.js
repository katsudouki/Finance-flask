
$(document).ready(function(){
    $('.panel li').click(function(){
        $('.panel li').removeClass('panelclicked');
        $(this).addClass('panelclicked');

    });
});
function carregarPagina(url) {
    // Atraso de 1500 milissegundos (1.5 segundos)
    setTimeout(function() {
        // Altera o atributo src do iframe
        document.getElementById("main").src = url;
    }, 100);
}
function reloadPagina(url) {
    // Atraso de 1500 milissegundos (1.5 segundos)
    setTimeout(function() {
        // Altera o atributo src do iframe
        window.location.reload();
    }, 200);
}