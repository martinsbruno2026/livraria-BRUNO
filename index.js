const readline = require("readline");

class Livro {
  constructor({ id, titulo, autor, categoria, paginas, preco, estoque }) {
    this.id = id;
    this.titulo = titulo;
    this.autor = autor;
    this.categoria = categoria;
    this.paginas = Number(paginas);
    this.preco = Number(preco);
    this.estoque = Number(estoque);
  }

  mostrarResumo() {
    return {
      id: this.id,
      titulo: this.titulo,
      autor: this.autor,
      categoria: this.categoria,
      paginas: this.paginas,
      preco: this.preco.toFixed(2),
      estoque: this.estoque,
    };
  }
}

class Livraria {
  constructor() {
    this.livros = [
      new Livro({
        id: 1,
        titulo: "Dom Casmurro",
        autor: "Machado de Assis",
        categoria: "Romance",
        paginas: 256,
        preco: 39.9,
        estoque: 12,
      }),
      new Livro({
        id: 2,
        titulo: "O Pequeno Príncipe",
        autor: "Antoine de Saint-Exupéry",
        categoria: "Infantil",
        paginas: 96,
        preco: 24.9,
        estoque: 20,
      }),
      new Livro({
        id: 3,
        titulo: "A Revolução dos Bichos",
        autor: "George Orwell",
        categoria: "Ficção",
        paginas: 176,
        preco: 29.9,
        estoque: 8,
      }),
    ];
  }

  gerarId() {
    if (this.livros.length === 0) return 1;
    return Math.max(...this.livros.map((livro) => livro.id)) + 1;
  }

  adicionarLivro({ titulo, autor, categoria, paginas, preco, estoque }) {
    if (!titulo || !autor || !categoria || !paginas || !preco || !estoque) {
      throw new Error("Preencha todos os campos obrigatórios.");
    }

    const livro = new Livro({
      id: this.gerarId(),
      titulo,
      autor,
      categoria,
      paginas,
      preco,
      estoque,
    });

    this.livros.push(livro);
    return livro;
  }

  listarLivros() {
    return this.livros.map((livro) => livro.mostrarResumo());
  }

  buscarPorTitulo(titulo) {
    const termo = titulo.toLowerCase();
    return this.livros.filter((livro) =>
      livro.titulo.toLowerCase().includes(termo),
    );
  }

  buscarPorAutor(autor) {
    const termo = autor.toLowerCase();
    return this.livros.filter((livro) =>
      livro.autor.toLowerCase().includes(termo),
    );
  }

  buscarPorCategoria(categoria) {
    const termo = categoria.toLowerCase();
    return this.livros.filter((livro) =>
      livro.categoria.toLowerCase().includes(termo),
    );
  }

  venderLivro(id, quantidade = 1) {
    const livro = this.livros.find((item) => item.id === Number(id));

    if (!livro) {
      throw new Error("Livro não encontrado.");
    }

    const qtd = Number(quantidade);
    if (qtd <= 0 || !Number.isInteger(qtd)) {
      throw new Error("Quantidade inválida.");
    }

    if (livro.estoque < qtd) {
      throw new Error(
        `Estoque insuficiente para ${livro.titulo}. Disponíveis: ${livro.estoque}`,
      );
    }

    livro.estoque -= qtd;
    return {
      titulo: livro.titulo,
      quantidade: qtd,
      valorTotal: (livro.preco * qtd).toFixed(2),
      estoqueRestante: livro.estoque,
    };
  }

  atualizarEstoque(id, quantidade) {
    const livro = this.livros.find((item) => item.id === Number(id));

    if (!livro) {
      throw new Error("Livro não encontrado.");
    }

    const qtd = Number(quantidade);
    if (!Number.isInteger(qtd)) {
      throw new Error("Quantidade inválida.");
    }

    livro.estoque += qtd;
    return livro;
  }

  resumoEstatistico() {
    const totalLivros = this.livros.length;
    const totalEstoque = this.livros.reduce(
      (soma, livro) => soma + livro.estoque,
      0,
    );
    const valorEstoque = this.livros.reduce(
      (soma, livro) => soma + livro.preco * livro.estoque,
      0,
    );
    const categoriaMaisVendida = "N/A";

    return {
      totalLivros,
      totalEstoque,
      valorEstoque: valorEstoque.toFixed(2),
      categoriaMaisVendida,
    };
  }
}

function mostrarLivros(livros) {
  if (!livros.length) {
    console.log("Nenhum livro encontrado.");
    return;
  }

  console.log("\nLista de livros:");
  livros.forEach((livro) => {
    console.log(
      `ID: ${livro.id} | ${livro.titulo} | Autor: ${livro.autor} | Categoria: ${livro.categoria} | Preço: R$ ${livro.preco} | Estoque: ${livro.estoque}`,
    );
  });
}

function mostrarMenu() {
  console.log("\n=== LIVRARIA BRUNO ===");
  console.log("1. Adicionar livro");
  console.log("2. Listar livros");
  console.log("3. Buscar por título");
  console.log("4. Buscar por autor");
  console.log("5. Buscar por categoria");
  console.log("6. Vender livro");
  console.log("7. Atualizar estoque");
  console.log("8. Resumo");
  console.log("0. Sair");
}

function questionInterface(rl, pergunta) {
  return new Promise((resolve) => {
    rl.question(pergunta, (resposta) => resolve(resposta.trim()));
  });
}

async function main() {
  const livraria = new Livraria();
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  console.log("Bem-vindo(a) à livraria!");

  while (true) {
    mostrarMenu();
    const opcao = await questionInterface(rl, "Escolha uma opção: ");

    switch (opcao) {
      case "1": {
        try {
          const titulo = await questionInterface(rl, "Título: ");
          const autor = await questionInterface(rl, "Autor: ");
          const categoria = await questionInterface(rl, "Categoria: ");
          const paginas = await questionInterface(rl, "Páginas: ");
          const preco = await questionInterface(rl, "Preço: ");
          const estoque = await questionInterface(rl, "Estoque: ");

          const livro = livraria.adicionarLivro({
            titulo,
            autor,
            categoria,
            paginas,
            preco,
            estoque,
          });
          console.log(`Livro adicionado com sucesso: ${livro.titulo}`);
        } catch (erro) {
          console.log(`Erro: ${erro.message}`);
        }
        break;
      }

      case "2": {
        mostrarLivros(livraria.listarLivros());
        break;
      }

      case "3": {
        const titulo = await questionInterface(
          rl,
          "Digite o título para buscar: ",
        );
        const resultado = livraria.buscarPorTitulo(titulo);
        mostrarLivros(resultado.map((livro) => livro.mostrarResumo()));
        break;
      }

      case "4": {
        const autor = await questionInterface(
          rl,
          "Digite o autor para buscar: ",
        );
        const resultado = livraria.buscarPorAutor(autor);
        mostrarLivros(resultado.map((livro) => livro.mostrarResumo()));
        break;
      }

      case "5": {
        const categoria = await questionInterface(
          rl,
          "Digite a categoria para buscar: ",
        );
        const resultado = livraria.buscarPorCategoria(categoria);
        mostrarLivros(resultado.map((livro) => livro.mostrarResumo()));
        break;
      }

      case "6": {
        try {
          const id = await questionInterface(rl, "ID do livro: ");
          const quantidade = await questionInterface(rl, "Quantidade: ");
          const venda = livraria.venderLivro(id, quantidade);
          console.log("Venda realizada com sucesso:");
          console.log(venda);
        } catch (erro) {
          console.log(`Erro: ${erro.message}`);
        }
        break;
      }

      case "7": {
        try {
          const id = await questionInterface(rl, "ID do livro: ");
          const quantidade = await questionInterface(
            rl,
            "Quantidade para adicionar/remover: ",
          );
          const livro = livraria.atualizarEstoque(id, Number(quantidade));
          console.log(
            `Estoque atualizado: ${livro.titulo} agora com ${livro.estoque} unidades.`,
          );
        } catch (erro) {
          console.log(`Erro: ${erro.message}`);
        }
        break;
      }

      case "8": {
        console.log(livraria.resumoEstatistico());
        break;
      }

      case "0": {
        console.log("Até logo!");
        rl.close();
        process.exit(0);
      }

      default:
        console.log("Opção inválida.");
    }
  }
}

main();
