// EXTRAI O TOKEN DA URL
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

if(!token)
{
    alert("Token de redefinição ausente. Volte para a página principal.")
    location = "/";
}

const form_red = document.querySelector(".form-red");

form_red.addEventListener("submit", function(event){
    event.preventDefault();

    nova_senha_1 = document.querySelector("#senha-red-1")?.value || null;
    nova_senha_2 = document.querySelector("#senha-red-2")?.value || null;

    if(nova_senha_1 == null || nova_senha_2 == null)
    {
        alert("Você deve inserir a nova senha")
        return;
    }

    if(nova_senha_1 != nova_senha_2)
    {
        alert("As senhas devem ser idênticas")
        return;
    }

    if(nova_senha_1.length < 6)
    {
        alert("A senha deve ter pelo menos 6 caracteres")
        return;
    }

    dados = {
        nova_senha: nova_senha_1
    }

    fetch(`/redefinir-senha?token=${token}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dados)
    })
    .then(response =>{
        if(response.ok)
        {
            return response.json()
        }

        return response.json().then(errorData =>{
            throw new Error(errorData.mensagem || `Erro ${response.status}: Falha ao redefinir senha`);
        })
    })
    .then(data =>{
        alert(data.mensagem)
        location = "/";
    })
    .catch(error =>{
        alert(`Erro ao redefinir senha: ${error.message}`)
    })
})