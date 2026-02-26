const form = document.getElementById('form-transacao');
const inputDescricao = document.getElementById('descricao');
const inputValor = document.getElementById('valor');
const selectTipo = document.getElementById('tipo');
const listaTransacoes = document.getElementById('lista-transacoes');
const displaySaldo = document.getElementById('valor-saldo');

let saldoAtual = 0;

function formatarMoeda(valor) {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

form.addEventListener('submit', function(event) {
    event.preventDefault();

    const descricao = inputDescricao.value;
    const valor = parseFloat(inputValor.value); 
    const tipo = selectTipo.value;

    if (tipo === 'receita') {
        saldoAtual += valor;
    } else {
        saldoAtual -= valor; 
    }
    
    displaySaldo.innerText = formatarMoeda(saldoAtual);

    const itemLista = document.createElement('li');
    
    if (tipo === 'despesa') {
        itemLista.style.borderLeft = '5px solid #dc2626'; 
    } else {
        itemLista.style.borderLeft = '5px solid #166534'; 
    }


    itemLista.innerHTML = `
        <span><strong>${descricao}</strong></span>
        <span>${tipo === 'receita' ? '+' : '-'} ${formatarMoeda(valor)}</span>
    `;

    if (listaTransacoes.innerHTML.includes('Carregando transações...')) {
        listaTransacoes.innerHTML = ''; 
    }

    listaTransacoes.appendChild(itemLista);

    inputDescricao.value = '';
    inputValor.value = '';
});