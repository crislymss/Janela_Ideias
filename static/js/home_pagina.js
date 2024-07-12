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

document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const line = document.getElementById('line');

    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const linkRect = link.getBoundingClientRect();
            const parentRect = link.parentElement.getBoundingClientRect();

            line.style.width = linkRect.width + 'px';
            line.style.left = linkRect.left - parentRect.left + 'px';

            // Optional: Smooth scroll to section
            document.querySelector(link.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

