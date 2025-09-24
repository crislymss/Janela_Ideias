/**
 * @description Cria um Intersection Observer para adicionar a classe 'visible'
 * aos elementos quando eles entram na área visível da tela (viewport).
 *
 * @logic
 * 1. Um IntersectionObserver é instanciado. A função de callback que ele recebe
 * será executada sempre que a visibilidade de um elemento alvo mudar.
 * 2. O callback itera por todas as entradas (entries) acionadas. Se uma entrada
 * estiver cruzando a área visível (ou seja, 'isIntersecting' é true), a
 * classe 'visible' é adicionada ao seu elemento alvo.
 * 3. Ele busca no DOM por todos os elementos com a classe '.reveal-on-scroll'.
 * 4. Ele percorre esses elementos selecionados e instrui o observador a começar
 * a monitorar cada um deles para mudanças de visibilidade.
 */
const observer = new IntersectionObserver((entries) => {
  // Itera sobre as entradas
  entries.forEach((entry) => {
    // Se o elemento estiver visível
    if (entry.isIntersecting) {
      // Adiciona a classe 'visible' a ele
      entry.target.classList.add('visible');
    }
  });
});

// Obtém todos os elementos com a classe 'reveal-on-scroll'
const elementsToReveal = document.querySelectorAll('.reveal-on-scroll');
// Instrui o observador a monitorar cada um desses elementos
elementsToReveal.forEach((el) => observer.observe(el));


/* NOTA: Existem duas implementações de carrossel abaixo. 
  A segunda é mais completa, com cálculo de cards visíveis e desativação de botões.
  A primeira foi deixada como no original, mas pode ser redundante.
*/

/**
 * @description Inicializa a funcionalidade de um carrossel horizontal após o
 * documento HTML ter sido completamente carregado.
 *
 * @logic
 * 1. Um event listener aguarda o evento 'DOMContentLoaded' para garantir que todos
 * os elementos HTML estejam disponíveis antes que o script seja executado.
 * 2. Ele seleciona os principais elementos do DOM: o trilho (track) que contém os
 * cards, os cards individuais e os botões de navegação.
 * 3. Ele calcula a largura de um único card, incluindo uma margem de 20px, para
 * determinar a distância de cada deslize.
 * 4. A função `moveToCard` gerencia a lógica de deslizamento. Ela calcula o valor
 * `translateX` necessário com base no índice do card de destino e na largura
 * do card, e então o aplica como uma transformação CSS no trilho.
 * 5. Verificações de limite são incluídas em `moveToCard` para impedir que o
 * carrossel deslize para além do início ou do fim do conteúdo. Nota: o limite
 * final `cards.length - 3` implica que o carrossel foi projetado para mostrar
 * três cards por vez.
 * 6. Event listeners de clique são adicionados aos botões de próximo e anterior,
 * que chamam `moveToCard` com o novo índice de destino para mover o carrossel.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Seleciona os elementos do carrossel
  const track = document.querySelector('.carousel-track');
  const cards = Array.from(track.children);
  const nextButton = document.getElementById('nextBtn');
  const prevButton = document.getElementById('prevBtn');

  // Verifica se os elementos existem antes de continuar
  if (!track || !cards.length || !nextButton || !prevButton) {
    console.log('Elementos do carrossel não encontrados');
    return;
  }

  // Calcula a largura de um card mais sua margem (assumida como 20px)
  const cardWidth = cards[0].getBoundingClientRect().width + 20;

  // Rastreia a posição atual do carrossel
  let currentIndex = 0;

  // Função para mover o trilho para o card correto
  const moveToCard = (targetIndex) => {
    // Verificação de limite: impede o deslize para antes do primeiro card
    if (targetIndex < 0) {
      targetIndex = 0;
      // Verificação de limite: impede o deslize para além do último conjunto de cards
    } else if (targetIndex > cards.length - 3) {
      targetIndex = cards.length - 3;
    }

    // Aplica a transformação CSS para deslizar o trilho
    track.style.transform = 'translateX(-' + (targetIndex * cardWidth) + 'px)';
    currentIndex = targetIndex;
  }

  // Event listener para o botão 'próximo'
  nextButton.addEventListener('click', () => {
    moveToCard(currentIndex + 1);
  });

  // Event listener para o botão 'anterior'
  prevButton.addEventListener('click', () => {
    moveToCard(currentIndex - 1);
  });
});


/**
 * @description Rola a página suavemente para a seção "quem-somos" quando chamada.
 * Ideal para ser usada como um handler de evento de clique em um botão.
 *
 * @logic
 * 1. Procura no DOM por um elemento com o ID 'quem-somos'.
 * 2. Se o elemento for encontrado, utiliza o método `scrollIntoView` com a
 * opção `behavior: 'smooth'` para criar uma animação de rolagem suave até ele.
 */
function explorar() {
  // Scroll para a seção "quem-somos"
  const quemSomosSection = document.getElementById('quem-somos');
  if (quemSomosSection) {
    quemSomosSection.scrollIntoView({
      behavior: 'smooth'
    });
  }
}

/**
 * @description Inicializa uma versão aprimorada do carrossel que calcula
 * dinamicamente os limites e desativa os botões de navegação quando o
 * início ou o fim é alcançado.
 *
 * @logic
 * 1. Aguarda o DOM estar completamente carregado.
 * 2. Seleciona os elementos do carrossel e calcula dinamicamente quantos cards
 * são visíveis com base na largura do contêiner e dos cards.
 * 3. Calcula o índice máximo (`maxIndex`) para o qual o carrossel pode rolar
 * sem mostrar espaço em branco no final.
 * 4. A função `updateNavButtons` verifica a posição atual (`currentIndex`) e
 * adiciona ou remove a classe 'disabled' e o atributo `disabled` dos botões
 * de navegação, impedindo cliques desnecessários.
 * 5. A função `moveToCard` move o carrossel e, em seguida, chama `updateNavButtons`
 * para garantir que o estado dos botões esteja sempre correto.
 * 6. Adiciona event listeners aos botões de navegação e chama `updateNavButtons`
 * uma vez no início para definir o estado inicial correto (o botão "anterior"
 * começa desativado).
 */
document.addEventListener('DOMContentLoaded', () => {
  const track = document.querySelector('.carousel-track');
  const cards = Array.from(track.children);
  const nextButton = document.getElementById('nextBtn');
  const prevButton = document.getElementById('prevBtn');

  if (!track || cards.length === 0 || !nextButton || !prevButton) {
    console.error('Elementos do carrossel não foram encontrados.');
    return;
  }

  const cardWidth = cards[0].offsetWidth + 20;
  const containerWidth = document.querySelector('.carousel-container').offsetWidth;
  const cardsVisible = Math.round(containerWidth / cardWidth);

  let currentIndex = 0;
  const maxIndex = cards.length - cardsVisible;

  // Função para atualizar a aparência e o estado dos botões
  const updateNavButtons = () => {
    // Botão "Anterior"
    if (currentIndex === 0) {
      prevButton.classList.add('disabled');
      prevButton.disabled = true;
    } else {
      prevButton.classList.remove('disabled');
      prevButton.disabled = false;
    }

    // Botão "Próximo"
    if (currentIndex >= maxIndex) {
      nextButton.classList.add('disabled');
      nextButton.disabled = true;
    } else {
      nextButton.classList.remove('disabled');
      nextButton.disabled = false;
    }
  }

  const moveToCard = (targetIndex) => {
    if (targetIndex < 0) {
      targetIndex = 0;
    } else if (targetIndex > maxIndex) {
      targetIndex = maxIndex;
    }

    track.style.transform = 'translateX(-' + (targetIndex * cardWidth) + 'px)';
    currentIndex = targetIndex;

    // Atualiza os botões após cada movimento
    updateNavButtons();
  }

  nextButton.addEventListener('click', () => {
    moveToCard(currentIndex + 1);
  });

  prevButton.addEventListener('click', () => {
    moveToCard(currentIndex - 1);
  });

  // Inicia os botões no estado correto
  updateNavButtons();
});

/**
 * @description Rola a página suavemente para a seção "como-participar"
 * quando chamada.
 *
 * @logic
 * 1. Procura no DOM por um elemento com o ID 'como-participar'.
 * 2. Se o elemento for encontrado, utiliza o método `scrollIntoView` com a
 * opção `behavior: 'smooth'` para rolar a página até ele.
 */
function participar() {
  // Scroll para a seção "como-participar"
  const comoParticiparSection = document.getElementById('como-participar');
  if (comoParticiparSection) {
    comoParticiparSection.scrollIntoView({
      behavior: 'smooth'
    });
  }
}

/**
 * @description Adiciona ou remove a classe 'rolagem' do cabeçalho (<header>)
 * com base na posição de rolagem da página. Útil para aplicar estilos
 * quando o usuário rola a página, como um fundo sólido ou uma sombra.
 *
 * @logic
 * 1. Um event listener é adicionado ao evento 'scroll' da janela.
 * 2. Sempre que o usuário rola a página, a função de callback é executada.
 * 3. Ela seleciona o elemento <header>.
 * 4. Utiliza `classList.toggle` com um segundo argumento booleano (`window.scrollY > 0`).
 * Isso adiciona a classe 'rolagem' se o usuário rolou para baixo (scrollY > 0) e
 * a remove se ele está no topo (scrollY === 0).
 */
window.addEventListener("scroll", function() {
  // Seleciona a tag <header> corretamente
  const header = document.querySelector("header");

  // Adiciona a classe 'rolagem' se a rolagem for maior que 0, senão remove
  header.classList.toggle("rolagem", window.scrollY > 0);
});

/**
 * @description Copia um endereço de e-mail pré-definido para a área de
 * transferência do usuário e exibe um alerta de confirmação.
 *
 * @logic
 * 1. Cria um elemento <input> temporário na memória.
 * 2. Define o valor desse input para o endereço de e-mail "propesqi@ufpi.edu.br".
 * 3. Anexa o input ao corpo do documento (necessário para que `select()` funcione).
 * 4. Seleciona o conteúdo do input.
 * 5. Executa o comando "copy" do navegador, que copia o texto selecionado.
 * 6. Remove o input temporário do documento para não deixar lixo no HTML.
 * 7. Exibe um alerta para informar ao usuário que a cópia foi bem-sucedida.
 */
function copyEmail() {
  var tempInput = document.createElement("input");
  tempInput.value = "propesqi@ufpi.edu.br";
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand("copy");
  document.body.removeChild(tempInput);
  alert("Endereço de email copiado!");
}