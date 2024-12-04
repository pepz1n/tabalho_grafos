import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations


def calcular_menor_caminho(grafo, partida):
    vertices = list(grafo.keys())
    if partida not in vertices:
        return None, None, f"A casa de partida '{partida}' não existe no grafo."

    vertices.remove(partida)
    menor_custo = float("inf")
    melhor_caminho = None

    for perm in permutations(vertices):
        caminho_atual = [partida] + list(perm)
        custo_atual = 0
        valido = True

        for i in range(len(caminho_atual) - 1):
            casa_atual, proxima_casa = caminho_atual[i], caminho_atual[i + 1]
            if proxima_casa in grafo[casa_atual]:
                custo_atual += grafo[casa_atual][proxima_casa]
            else:
                valido = False
                break

        if valido and custo_atual < menor_custo:
            menor_custo = custo_atual
            melhor_caminho = caminho_atual

    return melhor_caminho, menor_custo, None


def calcular_caminho():
    try:
        entrada_texto = entrada.get("1.0", tk.END).strip()
        partida = entrada_partida.get().strip()
        linhas = entrada_texto.split("\n")
        grafo = {}

        for linha in linhas:
            if linha:
                casa1, casa2, tempo = linha.split()
                casa1, casa2, tempo = casa1.strip(), casa2.strip(), int(tempo)
                if casa1 not in grafo:
                    grafo[casa1] = {}
                if casa2 not in grafo:
                    grafo[casa2] = {}
                grafo[casa1][casa2] = tempo
                grafo[casa2][casa1] = tempo

        melhor_caminho, menor_custo, erro = calcular_menor_caminho(grafo, partida)
        if erro:
            messagebox.showerror("Erro", erro)
        elif melhor_caminho is None:
            messagebox.showerror(
                "Erro", "Não foi possível encontrar um caminho que conecte todas as casas."
            )
        else:
            messagebox.showinfo(
                "Resultado",
                f"Melhor Caminho de Entrega: {' -> '.join(map(str, melhor_caminho))}\n"
                f"Tempo Total: {menor_custo} minutos",
            )
            visualizar_grafo(grafo, melhor_caminho)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


def visualizar_grafo(grafo, caminho=None):
    G = nx.Graph()
    for casa, conexoes in grafo.items():
        for vizinho, tempo in conexoes.items():
            G.add_edge(casa, vizinho, weight=tempo)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=800, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    if caminho:
        caminho_arestas = [(caminho[i], caminho[i + 1]) for i in range(len(caminho) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=caminho_arestas, edge_color="red", width=2)

    plt.title("Mapa de Entregas")
    plt.show()


janela = tk.Tk()
janela.title("Sistema de Entregas - Caminho Menos Custoso")

tk.Label(
    janela,
    text="Insira as conexões entre as casas no formato:\n"
    "Casa1 Casa2 Tempo\n(Exemplo: A B 10)",
).pack()
entrada = tk.Text(janela, height=10, width=50)
entrada.pack()

tk.Label(janela, text="Insira a casa de partida:").pack()
entrada_partida = tk.Entry(janela)
entrada_partida.pack()

tk.Button(janela, text="Calcular Caminho", command=calcular_caminho).pack()

janela.mainloop()
