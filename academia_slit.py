import random
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Classe Academia
class Academia:
    def __init__(self, halteres):
        self.halteres = halteres
        self.porta_halteres = {}
        self.reiniciar_o_dia()

    def reiniciar_o_dia(self):
        self.porta_halteres = {i: i for i in self.halteres}

    def listar_halteres(self):
        return [i for i in self.porta_halteres.values() if i != 0]

    def listar_espacos(self):
        return [i for i, j in self.porta_halteres.items() if j == 0]
    
    def pegar_haltere(self, peso):
        halt_pos = list(self.porta_halteres.values()).index(peso)
        key_halt = list(self.porta_halteres.keys())[halt_pos]
        self.porta_halteres[key_halt] = 0
        return peso
    
    def devolver_halter(self, pos, peso):
        self.porta_halteres[pos] = peso

    def calcular_caos(self):
        num_caos = [i for i, j in self.porta_halteres.items() if i != j]
        return len(num_caos) / len(self.porta_halteres)

# Classe Usuario
class Usuario:
    def __init__(self, tipo, academia):
        self.tipo = tipo  # 1 Normal - 2 Bagunceiro
        self.academia = academia
        self.peso = 0

    def iniciar_treino(self):
        lista_pesos = self.academia.listar_halteres()
        if not lista_pesos:
            return False  # Nenhum haltere disponível
        self.peso = random.choice(lista_pesos)
        self.academia.pegar_haltere(self.peso)
        return True

    def finalizar_treino(self):
        espacos = self.academia.listar_espacos()
        if self.tipo == 1:  # Usuário normal
            if self.peso in espacos:
                self.academia.devolver_halter(self.peso, self.peso)
            else:
                pos = random.choice(espacos)
                self.academia.devolver_halter(pos, self.peso)
        elif self.tipo == 2:  # Usuário bagunceiro
            pos = random.choice(espacos)
            self.academia.devolver_halter(pos, self.peso)
        self.peso = 0

# Função para simular e coletar caos
def simular_caos(halteres, num_usuarios, num_iteracoes):
    academia = Academia(halteres)
    usuarios = [Usuario(1, academia) for _ in range(num_usuarios)]  # Usuários normais
    usuarios += [Usuario(2, academia) for _ in range(1)]  # 1 usuário bagunceiro
    random.shuffle(usuarios)

    list_chaos = []

    for _ in range(num_iteracoes):
        academia.reiniciar_o_dia()
        for _ in range(10):  # Simula 10 ciclos
            random.shuffle(usuarios)
            for user in usuarios:
                user.iniciar_treino()
            for user in usuarios:
                user.finalizar_treino()
        list_chaos.append(academia.calcular_caos())

    return list_chaos

# Configuração do Streamlit
st.title("Simulação de Academia e Análise de Caos")
st.sidebar.title("Configurações")

# Escolha de cenários
cenario = st.sidebar.selectbox(
    "Escolha o cenário de halteres e usuários:",
    [
        "10-36 halteres e 10 usuários",
        "10-100 halteres e 20 usuários",
        "10-200 halteres e 30 usuários",
    ],
)

# Configurações baseadas no cenário escolhido
if cenario == "10-36 halteres e 10 usuários":
    halteres = [i for i in range(10, 36) if i % 2 == 0]
    num_usuarios = 10
elif cenario == "10-100 halteres e 20 usuários":
    halteres = [i for i in range(10, 100) if i % 2 == 0]
    num_usuarios = 20
elif cenario == "10-200 halteres e 30 usuários":
    halteres = [i for i in range(10, 200) if i % 2 == 0]
    num_usuarios = 30

# Simulação
num_iteracoes = st.sidebar.slider("Número de iterações:", 10, 100, 50, 10)
st.sidebar.write(f"Executando {num_iteracoes} iterações...")

# Rodando a simulação
list_chaos = simular_caos(halteres, num_usuarios, num_iteracoes)

# Gráfico
st.subheader("Distribuição do Caos")
fig, ax = plt.subplots()
sns.histplot(list_chaos, kde=True, ax=ax)
ax.set_title("Distribuição do Índice de Caos")
ax.set_xlabel("Índice de Caos")
ax.set_ylabel("Frequência")
st.pyplot(fig)

# Estatísticas
st.subheader("Análise Estatística")
st.write(f"**Média do caos:** {sum(list_chaos) / len(list_chaos):.4f}")
st.write(f"**Máximo do caos:** {max(list_chaos):.4f}")
st.write(f"**Mínimo do caos:** {min(list_chaos):.4f}")
