window.addEventListener("scroll", function(){
    let haeder = document.querySelector("#header");
    haeder.classList.toggle("rolagem", window.scrollY > 0);
});

function copyEmail() {
    var tempInput = document.createElement("input");
    tempInput.value = "gaai@ufpi.edu.br";
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand("copy");
    document.body.removeChild(tempInput);
    alert("Endereço de email copiado!");
}


window.addEventListener("scroll", function() {
    let header = document.querySelector("#header");
    let logo = document.querySelector(".logo");
    let headerContainer = document.querySelector(".header-conteiner");
    let opcoes_menu = document.querySelector(".opcoes-menu");

    if (window.scrollY > 0) {
        headerContainer.classList.add("rolagem");
        logo.classList.add("rolagem");
        opcoes_menu.classList.add("rolagem");
    } else {
        headerContainer.classList.remove("rolagem");
        logo.classList.remove("rolagem");
        opcoes_menu.classList.remove("rolagem");
    }
});
