document.addEventListener('DOMContentLoaded', function() {
    console.log('Página carregada!');
    const foodsContainer = document.getElementById('foods-container');
    if (!foodsContainer) {
        console.error('Erro: #foods-container não encontrado!');
        return;
    }
    console.log('#foods-container encontrado');

    // Teste hardcoded: Adicione uma comida manualmente para ver se aparece
    foodsContainer.innerHTML = `
        <div class="comida">
            <img src="/static/img/feijoada.webp" alt="Feijoada" class="comida-imagem">
            <h1 class="comida-nome">Feijoada (Teste)</h1>
            <p>Brasil</p>
            <p class="descrição">Comida feita com carinho (teste).</p>
            <button class="btn-receita">Ver receita</button>
            <button class="favorite-btn">Favoritar</button>
        </div>
    `;
    console.log('Comida de teste adicionada');

    // Agora teste o fetch da API
    console.log('Tentando fetch da API...');
    fetch('/api/comidas')
        .then(response => {
            console.log('Resposta da API:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Dados da API:', data);
            if (data.length > 0) {
                console.log('API retornou dados! Substituindo teste...');
                foodsContainer.innerHTML = '';  // Limpa o teste
                data.forEach(food => {
                    const foodDiv = document.createElement('div');
                    foodDiv.className = 'comida';
                    foodDiv.innerHTML = `
                        <img src="/static/${food.image}" alt="${food.name}" class="comida-imagem">
                        <h1 class="comida-nome">${food.name}</h1>
                        <p>${food.country}</p>
                        <p class="descrição">${food.description}</p>
                        <button class="btn-receita">Ver receita</button>
                        <button class="favorite-btn" data-id="${food.id}">Favoritar</button>
                    `;
                    foodsContainer.appendChild(foodDiv);
                });
            } else {
                console.log('API retornou array vazio []');
            }
        })
        .catch(err => {
            console.error('Erro no fetch:', err);
        });
});