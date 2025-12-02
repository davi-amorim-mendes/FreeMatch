let etapa_cont = 0;
const etapas = document.querySelectorAll(".etapa");

function mostrar_etapa(etapa_atual)
{
    etapas.forEach(etapa => etapa.classList.remove("ativa"));
    etapas[etapa_atual].classList.add("ativa");
}

function proxima_etapa()
{
    if(etapa_cont < etapas.length - 1)
    {
        etapa_cont++;
        mostrar_etapa(etapa_cont);
    }
}

function voltar_etapa()
{
    if(etapa_cont > 0)
    {
        etapa_cont--;
        mostrar_etapa(etapa_cont);
    }
}

function form_cad()
{
    const div_form = document.querySelector(".form-cadastro");
    const logo = document.querySelector(".landing-logo")
    const landing_card = document.querySelector(".landing-card")
    const landing_footer = document.querySelector(".landing-footer")

    const div_login = document.querySelector(".form-entrar");

    if(typeof div_login != "undefined")
    {
        div_login.style.display = "none";
    }

    div_form.style.display = "flex";
    logo.style.display = "none";
    landing_card.style.display = "none";
    landing_footer.style.display = "none";

}

function voltar_cad()
{
    const div_form = document.querySelector(".form-cadastro");
    const logo = document.querySelector(".landing-logo")
    const landing_card = document.querySelector(".landing-card")
    const landing_footer = document.querySelector(".landing-footer")

    div_form.style.display = "none";
    logo.style.display = "flex";
    landing_card.style.display = "flex";
    landing_footer.style.display = "flex";
}

const formulario = document.querySelector(".form-cad");

function verificar_idade(datanasc)
{
    const hoje = new Date();
    const data_nascimento = new Date(datanasc);

    const data18 = new Date(
        hoje.getFullYear() - 18,
        hoje.getMonth(),
        hoje.getDate()
    );

    return data_nascimento <= data18;
}

function validar_email(email)
{
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regexEmail.test(email);
}

formulario.addEventListener("submit", function(event){
    event.preventDefault();

    const nome = document.querySelector("#nome-cad")?.value || null;
    const email = document.querySelector("#email-cad")?.value || null;
    const senha1 = document.querySelector("#senha1-cad").value;
    const senha2 = document.querySelector("#senha2-cad").value;
    const datanasc = document.querySelector("#datanasc")?.value || null;
    const genero = document.querySelector("input[name='genero']:checked")?.value || null;
    const genero_pref = document.querySelector("input[name='genero-pref']:checked")?.value || null;
    const relacionamento = document.querySelector("#relacionamento").value;
    const sobre = document.querySelector("#sobre")?.value || null;
    const interesses = Array.from(
        document.querySelectorAll("input[name='interesses']:checked")
    ).map(el => el.value);

    const interesses_qtd = interesses.length;

    if(nome == null)
    {
        alert("Você deve informar seu nome completo")
        return;
    }

    if(email == null)
    {
        alert("Você precisa informar um e-mail")
        return;
    }
    if(!validar_email(email))
    {
        alert("Você deve inserir um e-mail válido")
        return;
    }

    if(datanasc == null)
    {
        alert("Você precisa informar sua data de nascimento")
        return;
    }

    if(genero == null)
    {
        alert("Você precisa selecionar um gênero")
        return;
    }
    if(genero_pref == null)
    {
        alert("Você precisa selecionar sua preferência de gênero")
        return;
    }

    if(interesses_qtd < 5)
    {
        alert("Você precisa selecionar 5 interesses");
        return;
    }

    if(!verificar_idade(datanasc))
    {
        alert("Você precisa ser maior de idade para se cadastrar");
        return;
    }

    if(senha1.length < 6)
    {
        alert("A senha deve ter no mínimo 6 caracteres")
        return;
    }

    if(senha1 != senha2)
    {
        alert("As senhas devem ser idênticas");
        return;
    }

    usuario = {
        nome: nome,
        email: email,
        senha: senha1,
        data: datanasc,
        genero: genero,
        generoPref: genero_pref,
        relacionamento: relacionamento,
        sobre: sobre,
        interesses: interesses,
        nivel: "viewer"
    }

    fetch("/cadastro", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(usuario)
    })
    .then(response =>{
        if(response.ok)
        {
            return response.json();
        }

        return response.json().then(errorData =>{
            throw new Error(errorData.mensagem || `Erro ${response.status}: Falha no cadastro`);
        })
    })
    .then(data =>{
        alert(data.mensagem);
        location = "/";
    })
    .catch(error =>{
        alert(`Erro ao cadastrar: ${error.message}`);
    })
})

