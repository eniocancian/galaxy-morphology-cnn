<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-2.15%2B-orange?logo=tensorflow" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Acurácia_Teste-83.13%25-brightgreen" alt="Accuracy">
  <img src="https://img.shields.io/badge/Dataset-Galaxy_Zoo_SDSS-indigo" alt="Dataset">
  <img src="https://img.shields.io/badge/Licença-MIT-green" alt="License">
</p>

# 🌌 Galaxy Morphology Classification — Galaxy Zoo & Deep Learning

Classificação morfológica automatizada de galáxias utilizando Redes Neurais Convolucionais (CNN) desenvolvidas em **TensorFlow/Keras** sobre observações do *Sloan Digital Sky Survey (SDSS)* via desafio *Galaxy Zoo*.

O projeto aborda a distinção de estruturas galácticas complexas por meio de visão computacional, com foco particular na avaliação do comportamento do modelo em geometrias ambíguas, como discos vistos de perfil (*edge-on*) e colisões/fusões em andamento.

---

## 🎯 Classes Morfológicas

O problema foi modelado em **4 classes canônicas**:

0. **Elíptica (Elliptical):** Perfis esferoidais lisos com simetria radial e ausência de subestruturas ou braços.
1. **Espiral (Spiral):** Discos com braços espirais evidentes, núcleo definido e textura estelar proeminente.
2. **Disco de Borda (Edge-on):** Discos galácticos finos observados lateralmente, frequentemente com linhas de poeira equatorial (*dust lanes*).
3. **Irregular / Fusão (Merger/Irregular):** Galáxias assimétricas, perturbadas por forças de maré ou em processo ativo de coalescência.

---

## 📊 Conjunto de Dados e Particionamento

A base é composta por um subconjunto balanceado e curado de **10.000 imagens** ($128 \times 128 \times 3$), estruturada da seguinte forma:

* **Treino:** ~7.000 imagens
* **Validação:** ~1.500 imagens
* **Teste:** 1.500 imagens (**375 por classe**, avaliação estritamente balanceada)

Os mapeamentos de cada conjunto encontram-se registrados em `data/train_split.csv`, `data/val_split.csv` e `data/test_split.csv`.

---

## 📈 Desempenho e Treinamento

A CNN foi treinada ao longo de 20 épocas utilizando a função de perda *Categorical Crossentropy* e o otimizador Adam. O melhor ponto de generalização foi capturado na **Época 17** via *ModelCheckpoint*, preservando os pesos ótimos e prevenindo sobreajuste (*overfitting*):

| Métrica | Treino (Final) | Validação (Época 17) | Teste Inédito |
| :--- | :---: | :---: | :---: |
| **Acurácia** | ~92.8% | **83.80%** | **83.13%** |
| **Loss** | 0.18 | **0.46** | 0.49 |

<p align="center">
  <img src="reports/figures/curvas_aprendizagem_galaxy_cnn.png" width="90%" alt="Curvas de Treino e Validação">
</p>

---

## 🔬 Resultados no Conjunto de Teste (1.500 Galáxias)

O conjunto de teste inédito confirmou que o modelo não memorizou as amostras de treino, atingindo uma acurácia global balanceada de **83.13%**:

```text
=======================================================
RELATÓRIO DE CLASSIFICAÇÃO (TEST SET)
=======================================================
                 precision    recall  f1-score   support

       Elíptica     0.8674    0.8373    0.8521       375
        Espiral     0.9310    0.9360    0.9335       375
 Disco de Borda     0.8065    0.8667    0.8355       375
Irregular/Fusão     0.7179    0.6853    0.7012       375

       accuracy                         0.8313      1500
      macro avg     0.8307    0.8313    0.8306      1500
   weighted avg     0.8307    0.8313    0.8306      1500
```

<p align="center">
  <img src="reports/figures/matriz_confusao_galaxy_zoo.png" width="48%" alt="Matriz de Confusão">
  <img src="reports/figures/metricas_morfologia_galaxias.png" width="48%" alt="Métricas por Classe">
</p>

---

## 🔍 Análise de Erros e Diagnóstico Astrofísico

A auditoria dos **253 casos incorretos** no conjunto de teste revelou padrões associados à geometria projetada em 2D:

1. **Fusões vs. Discos de Borda (60 casos):** Caudas de maré gravitacional (*tidal tails*) geradas durante colisões esticam filamentos de matéria estelar que, na resolução de 128x128, simulam o perfil linear de discos espirais vistos de perfil.
2. **Fusões vs. Elípticas (35 casos):** Estágios finais de fusão geram remanescentes amorfos e difusos, que ativam filtros convolucionais associados ao perfil suave das galáxias elípticas.
3. **Robustez da classe Espiral:** Teve a melhor performance isolada (F1 = 0.9335), com baixa dispersão graças à simetria periódica e à alta frequência espacial dos braços espirais.

<p align="center">
  <img src="reports/figures/piores_erros_classificacao.png" width="95%" alt="Inspeção dos Piores Erros">
</p>

*A auditoria detalhada de cada erro encontra-se em `data/relatorio_erros_galaxy_zoo.csv`.*
