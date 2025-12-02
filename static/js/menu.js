function select(tipo)
{
    let i;
    const menu_explorar = document.querySelector("#menu-explorar");
    const menu_matches = document.querySelector("#menu-matches");
    const menu_chat = document.querySelector("#menu-chat");
    const menu_perfil = document.querySelector("#menu-perfil");
    const menu_btn = document.querySelectorAll(".menu-btn");

    for(i = 0; i < menu_btn.length; i++)
    {
        menu_btn[i].classList.remove("select");
    }

    if(tipo == 'explorar')
    {
        menu_explorar.classList.add("select");
    }
    else if(tipo == 'matches')
    {
        menu_matches.classList.add("select")
    }
    else if(tipo == 'chat')
    {
        menu_chat.classList.add("select")
    }
    else if(tipo == 'perfil')
    {
        menu_perfil.classList.add("select")
    }
}