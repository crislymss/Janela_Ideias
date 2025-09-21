// JavaScript para funcionalidades do catálogo

document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade de busca
    const searchInput = document.querySelector('.search-input');
    const startupCards = document.querySelectorAll('.startup-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            let visibleCount = 0;
            
            startupCards.forEach(card => {
                const startupName = card.querySelector('.startup-nome').textContent.toLowerCase();
                const startupDesc = card.querySelector('.startup-descricao').textContent.toLowerCase();
                const incubadora = card.querySelector('.incubadora').textContent.toLowerCase();
                const setor = card.querySelector('.setor-tag').textContent.toLowerCase();
                
                if (startupName.includes(searchTerm) || 
                    startupDesc.includes(searchTerm) || 
                    incubadora.includes(searchTerm) || 
                    setor.includes(searchTerm)) {
                    card.style.display = 'block';
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
        });
    }
    
    // Funcionalidade dos filtros
    const filtroIncubadoras = document.querySelectorAll('.filtro-select')[0];
    const filtroSetores = document.querySelectorAll('.filtro-select')[1];
    
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
            
            let matchSearch = true;
            let matchIncubadora = true;
            let matchSetor = true;
            
            // Verificar busca
            if (searchTerm) {
                matchSearch = startupName.includes(searchTerm) || 
                             startupDesc.includes(searchTerm) || 
                             incubadora.includes(searchTerm) || 
                             setor.includes(searchTerm);
            }
            
            // Verificar incubadora
            if (incubadoraSelecionada && incubadoraSelecionada !== 'Todas as incubadoras') {
                matchIncubadora = incubadora.includes(incubadoraSelecionada.toLowerCase());
            }
            
            // Verificar setor
            if (setorSelecionado && setorSelecionado !== 'Todos os setores') {
                matchSetor = setor.includes(setorSelecionado.toLowerCase());
            }
            
            if (matchSearch && matchIncubadora && matchSetor) {
                card.style.display = 'block';
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
    
    // Animação de entrada dos cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Aplicar animação aos cards
    startupCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

// Função para copiar email (reutilizada da home)
function copyEmail() {
    const email = 'propesqi@ufpi.edu.br';
    navigator.clipboard.writeText(email).then(function() {
        alert('Email copiado para a área de transferência!');
    });
}
