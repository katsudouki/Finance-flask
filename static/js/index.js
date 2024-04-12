$(document).ready(function(){
    $("#login-button").click(function(){
        var username = $("#login-username").val();
        var password = $("#login-password").val();
        $.post("/auth", { 
            username: username, 
            password: password 
        }, function(data, status){
            if(data.message === "True") {
                showAuthMessage("Autenticação bem-sucedida!");
                window.location.href = "/dashboard";
            } else {
                showAuthMessage("Credenciais inválidas.");
            }
        }, "json").fail(function() {
            showAuthMessage("Ocorreu um erro ao processar sua solicitação.");
        });
    });
});

function showAuthMessage(message){
    icon="<i class='bx bxs-error bx-tada' ></i> "
    $("#auth-message").html(icon+message).fadeIn(400).delay(4000).fadeOut(400);
}

