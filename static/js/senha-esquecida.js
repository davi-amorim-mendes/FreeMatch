function voltar_rec()
{
    location = "/";
}

const div_form = document.querySelector(".form-rec");

div_form.addEventListener("submit", function(event){
    event.preventDefault();

    const email = document.querySelector("#email-rec")?.value || null;

    if(email == null)
    {
        alert("Você precisa inserir seu e-mail")
        return;
    }

    dado = {
        email: email
    }

    fetch("/senha-esquecida", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dado)
    })
    .then(response =>{
        if(response.ok)
        {
            return response.json()
        }

        return response.json().then(errorData =>{
            throw new Error(errorData.mensagem || `Erro ${response.status}: Falha ao recuperar conta`);
        })
    })
    .then(data =>{
        alert(data.mensagem);
        location = "/";
    })
    .catch(error =>{
        alert(`Erro ao recuperar conta: ${error.message}`);
    })
})