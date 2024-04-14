 $(document).ready(function(){
    $.fn.makeeditable = function() {
        // Adicionar data-id com o valor da primeira <td> em cada linha
        $(this).find('tbody tr').each(function() {
            var id = $(this).find('td:first').text();
            $(this).find('.btn-editar, .btn-apagar').attr('data-id', id);
            $(this).append('<td><i class="btn-editar bx bx-edit-alt" data-id="' + id + '"></i><i class="btn-apagar bx bx-trash" data-id="' + id + '"></i></td>');
        });

        $('.btn-apagar').click(function(){
            var id = $(this).data('id');
            var data = JSON.stringify({ id: id, action: 'delete' });
            $.ajax({
                type: 'POST',
                url: '/api/',
                data: data,
                contentType: 'application/json',
                success: function(response){
                    // Faça algo com a resposta, se necessário
                }
            });
        });

        // Ação ao clicar em "Editar"
        $(document).on('click', '.btn-editar', function(){
            // Reverter a linha anterior para o estado original
            revertRow();

            var tr = $(this).closest('tr');
            // Tornar os campos editáveis
            tr.addClass('editing'); // Adiciona a classe 'editing' à linha em edição
            tr.find('td:not(:last-child)').each(function(){
                var valor = $(this).text();
                $(this).html('<input type="text" value="' + valor + '">');
            });
            // Substituir botão de editar por botão de salvar
            $(this).removeClass('btn-editar bx-edit-alt').addClass('btn-salvar bx bx-save').attr('data-action', 'edit');
        });

        $(document).on('click', '.btn-salvar', function(){
            var tr = $(this).closest('tr');
            var id = $(this).data('id'); // Aqui estava faltando esta linha para obter o ID
            var data = { id: id };

            // Percorrer todas as colunas exceto a última
            tr.find('td:not(:last-child)').each(function(index) {
                var columnName = $(this).closest('table').find('th').eq(index).text(); // Obter o nome da coluna a partir do th correspondente
                var value = $(this).find('input').val();
                data[columnName.toLowerCase()] = value;
            });

            // Enviar informações para a API
            $.ajax({
                type: 'POST',
                url: '/api/',
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(response){
                    // Reverter a linha para o estado original após o sucesso da operação
                    revertRow();
                }
            });
        });

        // Função para reverter a linha para o estado original
        function revertRow() {
            var editedRow = $('tr.editing');
            if (editedRow.length > 0) {
                // Restaurar os valores originais
                editedRow.find('td:not(:last-child)').each(function(){
                    var valor = $(this).find('input').val();
                    $(this).html(valor);
                });
                // Remover a classe de edição e o botão de salvar
                editedRow.removeClass('editing');
                editedRow.find('.btn-salvar').removeClass('btn-salvar bx bx-save').addClass('btn-editar bx bx-edit-alt');
            }
        }
    };


});
 