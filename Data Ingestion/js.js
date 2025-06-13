async function puxar_api() {
  try {
    const response = await axios.get("http://localhost:8000/api/v1/aparelhos");
    const aparelhos = response.data;
    const container = document.getElementById("aparelhos-container");

    aparelhos.forEach(element => {
      const aparelhoDiv = document.createElement('div');
      aparelhoDiv.classList.add('aparelho-card');

      aparelhoDiv.innerHTML = `
        <h2>${element.aparelho}</h2>
        <p><strong>Variação:</strong> ${element.variacao}</p>
        <p><strong>Carga:</strong> ${element.carga ? 'Sim' : 'Não'}</p>
        <p><strong>Séries:</strong> ${element.serie}</p>
        <p><strong>Repetições:</strong> ${element.repeticao}</p>
      `;

      container.appendChild(aparelhoDiv);
    });
  } catch (error) {
    console.error('Erro ao puxar API:', error);
  }
}

window.addEventListener('DOMContentLoaded', puxar_api);
