import pandas as pd
import numpy as np

# Definir o número de leads a serem simulados.
numero_de_leads = 2000

# Criar um DataFrame vazio.
data = pd.DataFrame()
data["id_lead"] = range(1, numero_de_leads + 1)

# ----------------- Variáveis de Perfil -----------------
# Distribuição de cargos com diferentes probabilidades.
cargos = {"CEO": 0.1, "Diretor": 0.15, "Gerente": 0.3, "Analista": 0.45}
data["cargo"] = np.random.choice(
    list(cargos.keys()), numero_de_leads, p=list(cargos.values())
)

# Setor de atuação da empresa.
setores = ["Tecnologia", "Finanças", "Saúde", "Varejo", "Manufatura", "Educação"]
data["setor"] = np.random.choice(setores, numero_de_leads)

# Tamanho da empresa.
tamanho_empresa = {"Pequena": 0.4, "Média": 0.4, "Grande": 0.2}
data["tamanho_empresa"] = np.random.choice(
    list(tamanho_empresa.keys()), numero_de_leads, p=list(tamanho_empresa.values())
)

# Fonte do lead, com algumas fontes mais valiosas que outras.
fontes = {"Indicação": 0.2, "Evento": 0.15, "Orgânico": 0.4, "Anúncio": 0.25}
data["fonte_do_lead"] = np.random.choice(
    list(fontes.keys()), numero_de_leads, p=list(fontes.values())
)

# Tags para qualificação do lead.
tags_list = ["Sem tag", "MQL", "SQL", "Cold", "Hot"]
data["tags"] = np.random.choice(tags_list, numero_de_leads)

# ----------------- Variáveis de Funil e Negócio -----------------
# Produto de interesse.
produtos = ["Plano Básico", "Plano Pro", "Plano Premium", "Consultoria"]
data["produto_de_interesse"] = np.random.choice(produtos, numero_de_leads)

# Lógica de preço: fixa para planos, variável para consultoria.
data["valor_investimento"] = 0
data.loc[data["produto_de_interesse"] == "Plano Básico", "valor_investimento"] = 500
data.loc[data["produto_de_interesse"] == "Plano Pro", "valor_investimento"] = 2500
data.loc[data["produto_de_interesse"] == "Plano Premium", "valor_investimento"] = 10000

# Consultoria tem valor variável.
# Geramos o array de valores aleatórios apenas para o subconjunto de "Consultoria".
consultoria_leads = data.loc[data["produto_de_interesse"] == "Consultoria"]
data.loc[data["produto_de_interesse"] == "Consultoria", "valor_investimento"] = (
    np.random.lognormal(mean=9.5, sigma=1.5, size=consultoria_leads.shape[0]).astype(
        int
    )
)

# Consultoria com valor maior para cargos de decisão.
consultoria_ceo_dir_leads = data.loc[
    (data["produto_de_interesse"] == "Consultoria")
    & (data["cargo"].isin(["CEO", "Diretor"]))
]
data.loc[
    (data["produto_de_interesse"] == "Consultoria")
    & (data["cargo"].isin(["CEO", "Diretor"])),
    "valor_investimento",
] = np.random.lognormal(
    mean=10.5, sigma=1.8, size=consultoria_ceo_dir_leads.shape[0]
).astype(
    int
)
data["valor_investimento"] = np.clip(data["valor_investimento"], 100, 500000)

# Etapa atual no funil de vendas.
etapas = ["Contato", "Qualificação", "Proposta", "Negociação", "Fechamento"]
data["etapa_do_funil"] = np.random.choice(etapas, numero_de_leads)

# Tempo na etapa atual, simulando que leads parados têm menos chance de conversão.
data["tempo_na_etapa"] = np.random.randint(1, 40, size=numero_de_leads)
data.loc[data["etapa_do_funil"] == "Negociação", "tempo_na_etapa"] = np.random.randint(
    15, 60, size=data.loc[data["etapa_do_funil"] == "Negociação"].shape[0]
)

# ----------------- Lógica da Conversão -----------------
# Probabilidade inicial de conversão.
probabilidade_base = 0.1

# Ajustar a probabilidade com base nas características do lead.
data["prob_conversao"] = probabilidade_base
data.loc[data["cargo"].isin(["CEO", "Diretor"]), "prob_conversao"] += 0.3
data.loc[data["tamanho_empresa"] == "Grande", "prob_conversao"] += 0.2
data.loc[data["fonte_do_lead"] == "Indicação", "prob_conversao"] += 0.15
data.loc[data["tags"] == "SQL", "prob_conversao"] += 0.2
data.loc[data["tags"] == "Hot", "prob_conversao"] += 0.3
data.loc[
    data["etapa_do_funil"].isin(["Negociação", "Fechamento"]), "prob_conversao"
] += 0.2

# Diminuir a chance para leads que estão parados.
data["prob_conversao"] -= (data["tempo_na_etapa"] / 100) * 0.3

# Aumentar a chance de conversão para leads com valor de investimento alto (principalmente consultoria).
data["prob_conversao"] += np.log1p(data["valor_investimento"] / 10000) * 0.1

# Criar a variável alvo 'Converteu' com base na probabilidade final.
data["convertido"] = np.random.binomial(1, data["prob_conversao"].clip(0, 1))

# Remover colunas auxiliares.
data = data.drop(columns=["prob_conversao"])

# ----------------- Salvar o Dataset -----------------
# Certifique-se de que a pasta 'data' existe.
# Use um caminho relativo para salvar o arquivo na pasta 'data'.
try:
    data.to_csv("../../data/dados_crm.csv", index=False)
    print("Dataset 'dados_crm.csv' gerado e salvo na pasta 'data/' com sucesso!")
except FileNotFoundError:
    print(
        "Erro: A pasta 'data' não foi encontrada. Crie a pasta e execute o script novamente."
    )
