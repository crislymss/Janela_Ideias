/**
 * @description Inicializa todas as funcionalidades interativas da página de catálogo
 * assim que o conteúdo HTML é completamente carregado.
 *
 * @logic
 * 1. Configura a barra de busca para filtrar os cards em tempo real.
 * 2. Configura os menus suspensos (filtros) para refinar os resultados.
 * 3. Cria um 'Intersection Observer' para animar os cards quando eles
 * aparecem na tela durante a rolagem.
 * 4. Implementa a rolagem suave para links internos (links âncora).
 */
document.addEventListener('DOMContentLoaded', function() {
    // --- Funcionalidade de busca ---
    const searchInput = document.querySelector('.search-input');
    const startupCards = document.querySelectorAll('.startup-card');

    if (searchInput) {
        // NOTA: Este listener de busca é funcional, mas sua lógica foi integrada
        // e aprimorada na função aplicarFiltros() para que a busca e os filtros
        // funcionem em conjunto. Pode ser considerado redundante se os filtros
        // sempre aplicarem a busca.
        searchInput.addEventListener('input', function() {
            aplicarFiltros(); // Chamada centralizada para garantir que tudo funcione junto
        });
    }

    // --- Funcionalidade dos filtros ---
    const filtroIncubadoras = document.querySelectorAll('.filtro-select')[0];
    const filtroSetores = document.querySelectorAll('.filtro-select')[1];

    /**
     * @description Filtra os cards de startups visíveis com base nos valores
     * selecionados nos filtros de incubadora, setor e no termo da busca.
     *
     * @logic
     * 1. Obtém os valores atuais dos filtros de incubadora, setor e da barra de busca.
     * 2. Itera sobre cada card de startup.
     * 3. Para cada card, verifica três condições: se corresponde ao termo da busca,
     * se corresponde à incubadora selecionada e se corresponde ao setor selecionado.
     * 4. O card só é exibido se todas as condições ativas forem verdadeiras.
     * Caso contrário, ele é ocultado com `display: 'none'`.
     * 5. Ao final, atualiza um contador na tela com o número de startups visíveis.
     */
    function aplicarFiltros() {
        const incubadoraSelecionada = filtroIncubadoras ? filtroIncubadoras.value : '';
        const setorSelecionado = filtroSetores ? filtroSetores.value : '';
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';

        let visibleCount = 0;

        startupCards.forEach(card => {
            const startupName = card.querySelector('.startup-nome').textContent.toLowerCase();
            const startupDesc = card.querySelector('.startup-descricao').textContent.toLowerCase();
            const incubadora = card.querySelector('.incubadora').textContent.toLowerCase();
            const setor = card.querySelector('.setor-tag').textContent.toLowerCase();

            // Condições de filtro
            const matchSearch = searchTerm === '' || startupName.includes(searchTerm) || startupDesc.includes(searchTerm) || incubadora.includes(searchTerm) || setor.includes(searchTerm);
            const matchIncubadora = incubadoraSelecionada === '' || incubadoraSelecionada === 'Todas as incubadoras' || incubadora.includes(incubadoraSelecionada.toLowerCase());
            const matchSetor = setorSelecionado === '' || setorSelecionado === 'Todos os setores' || setor.includes(setorSelecionado.toLowerCase());

            // Exibe o card apenas se todas as condições forem atendidas
            if (matchSearch && matchIncubadora && matchSetor) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Atualizar contador de resultados
        const resultadoBusca = document.querySelector('.resultado-busca span');
        if (resultadoBusca) {
            resultadoBusca.textContent = `${visibleCount} startups encontradas`;
        }
    }

    // Adicionar event listeners aos filtros
    if (filtroIncubadoras) {
        filtroIncubadoras.addEventListener('change', aplicarFiltros);
    }

    if (filtroSetores) {
        filtroSetores.addEventListener('change', aplicarFiltros);
    }

    // --- Animação de entrada dos cards ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    /**
     * @description Cria um observador que aplica uma animação de fade-in e slide-up
     * aos cards de startup quando eles entram na área visível da tela.
     *
     * @logic
     * 1. Um `IntersectionObserver` é criado para monitorar quando os cards entram na tela.
     * 2. Quando um card se torna visível (`isIntersecting`), sua opacidade é definida
     * como 1 e sua posição Y é resetada para 0, ativando a animação CSS.
     * 3. Antes de iniciar a observação, cada card é preparado: sua opacidade inicial
     * é 0, ele é movido 30px para baixo, e uma transição CSS é aplicada.
     * 4. Um atraso (`transition-delay`) escalonado é adicionado a cada card com base
     * em seu índice, criando um efeito de cascata visualmente agradável.
     */
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Aplicar animação e iniciar observação para cada card
    startupCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });

    // --- Smooth scroll para links internos ---
    /**
     * @description Implementa uma navegação com rolagem suave para todos os links
     * internos da página (aqueles que começam com '#').
     *
     * @logic
     * 1. Seleciona todos os links `<a>` cujo atributo `href` começa com '#'.
     * 2. Adiciona um listener de clique a cada um deles.
     * 3. No clique, previne o comportamento padrão do navegador (o salto imediato).
     * 4. Encontra o elemento de destino na página com base no `href` do link.
     * 5. Se o alvo existir, rola a tela suavemente até o topo dele.
     */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

/**
 * @description Copia um endereço de e-mail para a área de transferência do usuário
 * usando a API moderna e segura do navegador (`navigator.clipboard`).
 *
 * @logic
 * 1. Define o e-mail a ser copiado.
 * 2. Chama `navigator.clipboard.writeText()`, que retorna uma Promise.
 * 3. Quando a Promise é resolvida com sucesso, um alerta informa ao usuário
 * que o e-mail foi copiado.
 */
function copyEmail() {
    const email = 'propesqi@ufpi.edu.br';
    navigator.clipboard.writeText(email).then(function() {
        alert('Email copiado para a área de transferência!');
    });
}

/**
 * @description Encontra elementos numéricos na página e inicia uma animação de
 * contagem crescente para cada um.
 *
 * @logic
 * 1. Aguarda o carregamento completo do DOM.
 * 2. Seleciona todos os elementos com a classe `.numero`.
 * 3. Para cada elemento, armazena seu valor original (o número final) em um
 * atributo `data-target` e redefine seu texto visível para '0'.
 * 4. Chama a função `animateNumber` para cada elemento, dando início à animação.
 */
document.addEventListener("DOMContentLoaded", () => {
    /**
     * @description Anima o conteúdo de texto de um elemento, fazendo-o contar
     * de 0 até um número alvo (`data-target`) ao longo de uma duração definida.
     * @param {HTMLElement} element O elemento do DOM a ser animado.
     */
    const animateNumber = (element) => {
        const target = +element.getAttribute('data-target');
        let current = 0;
        const duration = 2000; // 2 segundos
        const stepTime = 10; // Intervalo de atualização
        const increment = target / (duration / stepTime);

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.innerText = target; // Garante o valor final exato
                clearInterval(timer); // Para a animação
            } else {
                element.innerText = Math.ceil(current);
            }
        }, stepTime);
    };

    const numberElements = document.querySelectorAll('.numero');
    numberElements.forEach(el => {
        const targetValue = el.innerText;
        el.setAttribute('data-target', targetValue);
        el.innerText = '0';
        animateNumber(el);
    });
});

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("menu-toggle");
  const nav = document.getElementById("nav-menu");

  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const open = toggle.classList.toggle("active");
    nav.classList.toggle("active");
    // para acessibilidade: informa se está aberto
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // Fecha menu ao clicar em um link (útil em mobile)
  nav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      if (nav.classList.contains("active")) {
        nav.classList.remove("active");
        toggle.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  });
});
