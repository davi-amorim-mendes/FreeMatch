function form_ent()
{
    const div_form = document.querySelector(".form-entrar");
    const landing_card = document.querySelector(".landing-card")
    const landing_footer = document.querySelector(".landing-footer")

    div_form.style.display = "flex";
    landing_card.style.display = "none";
    landing_footer.style.display = "none";

}

function voltar_ent()
{
    const div_form = document.querySelector(".form-entrar");
    const landing_card = document.querySelector(".landing-card")
    const landing_footer = document.querySelector(".landing-footer")

    div_form.style.display = "none";
    landing_card.style.display = "flex";
    landing_footer.style.display = "flex";
}

const formulario_login = document.querySelector(".form-ent");

formulario_login.addEventListener("submit", function(event){
    event.preventDefault();

    email = document.querySelector("#email-login").value;
    senha = document.querySelector("#senha-login").value;

    usuario = {
        email: email,
        senha: senha
    }

    fetch("/login", {
        method: "POST",
        credentials: "include",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(usuario)
    })
    .then(response =>{
        if(response.ok)
        {
            return response.json();
        }

        return response.json().then(errorData =>{
            throw new Error(errorData.mensagem || `Erro ${response.status}: Falha no login`)
        })
    })
    .then(data =>{
        alert(data.mensagem)
        location = "/home"
    })
    .catch(error =>{
        alert(`Erro ao logar: ${error.message}`)
    })
})