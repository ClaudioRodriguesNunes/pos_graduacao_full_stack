/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/equipamentos';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.equipamentos.forEach(item => insertList(item.tag, item.nome, item.periodo))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
Chamada inicial da função para carregar os dados.
*/

getList()

/*
Função para adicionar um item na lista do servidor via requisição POST.
*/

const postItem = async (inputTag, inputNome, inputPeriodo) => {
  const formData = new FormData();
  formData.append('pk_tag', inputTag);
  formData.append('nome', inputNome);
  formData.append('periodo', inputPeriodo);

  let url = 'http://127.0.0.1:5000/equipamento';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
Função para criar um botão de fechar para cada item da lista.
*/

const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
Função para remover um item da lista quando clicado no botão de fechar.
*/

const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const tagItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(tagItem)
        alert("Removido!")
      }
    }
  }
}

/*
Função para deletar um item da lista do servidor via requisição DELETE.
*/

const deleteItem = (tagItem) => {
  console.log("Deletando item com a TAG:",tagItem)
  let url = `http://127.0.0.1:5000/equipamento?pk_tag=${encodeURIComponent(tagItem)}`;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .then(data => {console.log("Delete response:", data)})
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
Função para adicionar um novo item na lista.
*/

const newItem = () => {
  let inputTag = document.getElementById("newTag").value;
  let inputNome = document.getElementById("newNome").value;
  let inputPeriodo = document.getElementById("newPeriodo").value;

  if (inputTag === '') {
    alert("Escreva a tag de um item!");
    return;
  } else if (inputNome === '') {
    alert("Escreva uma descrição do equipamento!");
    return;
  } else if (isNaN(inputPeriodo)){
    alert("Periodo deve ser um número")
    return;
  } else {
    insertList(inputTag, inputNome, inputPeriodo)
    postItem(inputTag, inputNome, inputPeriodo).then(() => {
      alert("Item adicionado com sucesso!");
      document.getElementById("newTag").value = "";
      document.getElementById("newNome").value = "";
      document.getElementById("newPeriodo").value = "";
    }) .catch(error => {
      console.error("Error adicionando item: ", error);
      alert("Falha ao adiocnar item. Verifique o console para mais detalhes.");
    })
  alert("Item adicionado!")
  }
}

/*
Função para inserir itens na tabela HTML.
*/

const insertList = (tagEquipamento, nome, periodo) => {
  var item = [tagEquipamento, nome, periodo]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newTag").value = "";
  document.getElementById("newNome").value = "";
  document.getElementById("newPeriodo").value = "";

  removeElement()
}