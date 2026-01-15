function logout()
{
    fetch("/logout", {
        method: "POST",
        credentials: "include",
    })
    .then(response =>{
        return response.json()
    })
    .then(data =>{
        alert(data.mensagem)
        location = "/"
    })
}

function select(tipo)
{
    switch(tipo)
    {
        case 'explorar':
            location = "/explorer";
            break;
        case 'matches':
            location = "/matches";
            break;
        case 'chat':
            location = "/chat";
            break;
        case 'perfil':
            location = "/perfil";
            break;
        case 'sair':
            if(confirm("Tem certeza de que deseja sair?"))
            {
                logout()
            }
            break;
    }
}