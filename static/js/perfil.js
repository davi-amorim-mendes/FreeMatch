function cookie(nome)
{
    return document.cookie.split("; ").find(row => row.startsWith(nome + "="))?.split("=")[1];
}

document.querySelector("#foto-perfil").addEventListener('change', function(){
    const foto = this.files[0];
    if(!foto) return;

    const csrfToken = cookie("csrf_access_token");

    const formData = new FormData();
    formData.append('foto-perfil', foto);

    fetch("/foto-perfil", {
        method: "POST",
        credentials: "include",
        headers: {"X-CSRF-TOKEN": csrfToken},
        body: formData
    })
    .then(response =>{
        if(response.ok){return response.json();}

        return response.json().then(errorData =>{
            throw new Error(errorData.mensagem || `Erro ${response.status}: Falha ao alterar imagem`)
        })
    })
    .then(data =>{
        alert(data.mensagem)
        const texto_foto = document.querySelector("#sem-foto");
        if (texto_foto) {
            texto_foto.remove();
        }
        const img_perfil = document.querySelector("#img-perfil");
        img_perfil.src = data.url;
    })
    .catch(error =>{
        alert(`Erro ao enviar imagem: ${error.message}`)
    })
})

function editar_sobre()
{
    novo_sobre = prompt("Digite sua nova bio.")
    const csrfToken = cookie("csrf_access_token");

    fetch("/editar-sobre", {
        method: "POST",
        credentials: "include",
        headers: {"X-CSRF-TOKEN": csrfToken, "Content-Type": "application/json"},
        body: JSON.stringify(novo_sobre)
    })
    .then(response =>{
        return response.json()
    })
    .then(data =>{
        alert(data.mensagem)
        const sobre = document.querySelector("#usuario-sobre-texto")
        sobre.textContent = novo_sobre
    })
}