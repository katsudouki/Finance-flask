$(document).ready(function(){

    
    $.fn.makeeditable = function(categories, selectColumnIndex,checkboxColumnIndex,tabela) {

        $(this).find('thead tr:not(:first)').append('<th scope="col">Opções</th>')
        // INFO: Adicionar data-id com o valor da primeira <td> em cada linha
        $(this).find('tbody tr').each(function() {
            var id = $(this).find('td:first').text();
            $(this).find('.btn-editar, .btn-apagar').attr('data-id', id);
            $(this).append('<td><i class="btn-editar bx bx-edit-alt" data-id="' + id + '"></i><i class="btn-apagar bx bx-trash" data-id="' + id + '"></i></td>');
        });

        // INFO: Ação ao clicar em "Editar"
        $(document).on('click', '.btn-editar', function(){
            revertRow();
            var tr = $(this).closest('tr');
            tr.addClass('editing');
            tr.find('td:not(:last-child)').each(function(index){
                var valor = $(this).text();
                if (index === selectColumnIndex) {
                    // INFO: pega o index da coluna e transforma o td respectivo em campos select
                    var selectOptions = '';
                    $.each(categories, function(i, category) {
                        selectOptions += '<option value="' + category + '">' + category + '</option>';
                    });
                    $(this).html('<select style="align:center !important;margin-left:20px;background-color:#d0d0d0 !important;" class="category  form-select">' + selectOptions + '</select>');
                    $(this).find('.category').val(valor);
                }
                else if (index === checkboxColumnIndex) {
                    valor=$('#pagoc').prop('checked');
                    if (String(valor)=="true") {
                        console.log("funcionando")
                    $(this).html('<input type="checkbox" id="pagoc" value="' + valor + '" checked >');

                    }else {
                        console.log(valor)
                        $(this).html('<input type="checkbox"  id="pagoc" value="' + valor + '" >');}
                } 
                else {
                    $(this).html('<input type="text" value="' + valor + '">');
                }
            });
            // INFO: Substituir botão de editar por botão de salvar
            $(this).removeClass('btn-editar bx-edit-alt').addClass('btn-salvar bx bx-save').attr('data-action', 'edit');
        });

        $(document).on('click', '.btn-salvar', function(){
            var tr = $(this).closest('tr');
            var id = $(this).data('id');
            var tipot="";
            if (tabela == "lucros") {
    console.log("Tabela é lucros");
    tipot = "insertlucro";
} else if (tabela == "dividas") {
    tipot = "insertpreju";
} else {
    console.log(tabela);
}
            var data = {tabela:tabela,type:tipot};

            // INFO: Pega todas as colunas exceto a última
          tr.find('td:not(:last-child)').each(function(index) {
          var columnName = $(this).closest('table').find('th:not(:last-child)').eq(index).text();
          var value;
          if (index === selectColumnIndex) {
          // INFO: Se for a coluna especificada para ser um <select>, obter o valor do <select>
          value = $(this).find('.category').val();
          $(this).text(value);
          } 
          else if (index === checkboxColumnIndex) {
          
          value = $('#pagoc').prop('checked');
          

          
          } 

          else {
             value = $(this).find('input').val();
            }
          data[columnName.toLowerCase()] = value;
        });

            $.ajax({
                type: 'POST',
                url: '/api/',
               
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(response){
                    revertRow();
                }
            });
        reloadPagina('/entradas')
        });



 $(document).on('click', '.btn-apagar', function(){
            var tr = $(this).closest('tr');
            var id = $(this).data('id');
            var data = { id: id,tabela:tabela,type:'delete' };
            $.ajax({
                type: 'POST',
                url: '/api/',
               
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(response){
                    revertRow();
                }
            });
           reloadPagina('/entradas')
        });


        // INFO: Função para reverter a linha para o estado original
        function revertRow() {
            var editedRow = $('tr.editing');
            if (editedRow.length > 0) {
                // Restaurar os valores originais
                editedRow.find('td:not(:last-child)').each(function(index){
                    var valor;
                    if (index === selectColumnIndex) {
                        valor = $(this).text();
                    } else if(index === checkboxColumnIndex){
                        valor =$('#pago').prop('checked');
                    }
                    else {
                        valor = $(this).find('input').val();
                    }
                    $(this).html(valor);
                });
                editedRow.removeClass('editing');
                editedRow.find('.btn-salvar').removeClass('btn-salvar bx bx-save').addClass('btn-editar bx bx-edit-alt');
            }
        }
        

        // INFO: Adicionar nova linha duplicando a última linha ao clicar em #addbutton
$('#addbutton').on('click', function() {
    var lastRow = $('tbody tr:last');
    var newId ="0";
    var newRow = lastRow.clone();
    newRow.removeClass('hidden'); // Remover a classe 'hidden' da nova linha
    newRow.find('td:first').text(newId);
    newRow.find('td:not(:first-child):not(:last-child)').not(':has(i)').text('');
    // INFO: Definir os data-id de acordo com o valor da primeira td
    newRow.find('.btn-editar, .btn-apagar').attr('data-id', newId);

    $('tbody').append(newRow);
});

    };
});
