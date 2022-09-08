from matplotlib.figure import Figure
import base64
import numpy as np
from io import BytesIO
from statistics import mean, stdev
from static.scripts.MontaSagresSimba import *


def criar_plot_1(empenho):
    # gerar a figura (sem utilizar o pyploy)
    fig = Figure(figsize=(7, 5))
    ax = fig.subplots()

    y = empenho.listValoresPagamentos
    x = empenho.datasPagamentosDateTime
    ax.plot(x, y, color="black", linestyle="--", marker="o")

    # arrumar as datas no eixo X
    avg = mean(y)
    std = stdev(y)
    lower_bound = []
    upper_bound = []
    for i in range(len(y)):
        lower_bound.append(avg - std)
        upper_bound.append(avg + std)

    ax.fill_between(x, lower_bound, upper_bound, alpha=0.2)
    fig.autofmt_xdate()

    # estilo
    ax.set_xlabel("Data Pagamento")
    ax.set_ylabel("Valor (R$)")

    # salvar imagem temporarimente em um buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # embed the result in the html output.
    data_image = base64.b64encode(buf.getbuffer()).decode("ascii")

    image_file = open("./static/assets/plot.png", "wb")
    image_file.write(base64.b64decode((data_image)))
    image_file.close()


def criar_plot_2(empenho):
    # gerar a figura (sem utilizar o pyploy)
    fig = Figure(figsize=(7, 5))
    ax = fig.subplots()

    y = empenho.listValoresPagamentos
    x = empenho.datasPagamentosDateTime

    # arrumar as datas no eixo X
    ax.plot(x, y, color="black", linestyle="--", marker="o")
    fig.set_size_inches(7.41, 5)

    avg = mean(y)
    std = stdev(y)

    lb = []
    ub = []
    for i in range(len(y)):
        lb.append(avg - std)
        ub.append(avg + std)

    ax.fill_between(x, lb, ub, alpha=0.2)
    fig.autofmt_xdate()

    # estilo
    ax.set_xlabel("Data Pagamento")
    ax.set_ylabel("Valor (R$)")

    # salvar imagem temporarimente em um buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # embed the result in the html output.
    data_image = base64.b64encode(buf.getbuffer()).decode("ascii")

    image_file = open("./static/assets/plot.png", "wb")
    image_file.write(base64.b64decode((data_image)))
    image_file.close()


def criar_plot_3(idx):
    lObjs = montaObjsSagresSimba(
        "../datasets/simba/SimbaGoiana.csv", "../datasets/simba/SagresGoiana.csv"
    )

    # gerar a figura (sem utilizar o pyploy)
    fig = Figure(figsize=(7, 5))
    ax = fig.subplots()

    barWidth = 0.25
    r1 = np.arange(12)
    r2 = [x + barWidth for x in r1]

    dictPagsSagres = lObjs[idx].dictPagsMensaisSagres
    dictPagsSimba = lObjs[idx].dictPagsMensaisSimba

    gastosSagres = []
    gastosSimba = []

    for i in range(1, 13):
        gastosSagres.append(dictPagsSagres[i])
        gastosSimba.append(dictPagsSimba[i])

    ax.bar(r1, gastosSagres, color="#6A5ACD", width=barWidth, label="Sagres")
    ax.bar(r2, gastosSimba, color="#00BFFF", width=barWidth, label="Simba")

    ax.ticklabel_format(style="plain")
    ax.set(
        title="Destino: " + str(lObjs[idx].nmFornecedor),
        xlabel="Mês",
        ylabel="Valor Mensal (R$)",
    )
    ax.set_xticklabels(
        [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez",
        ]
    )
    ax.set_xticks([r + barWidth for r in range(12)])  # ,
    ax.legend(loc="upper right")

    fig.autofmt_xdate()

    # salvar imagem temporarimente em um buffer
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # embed the result in the html output.
    data_image = base64.b64encode(buf.getbuffer()).decode("ascii")

    image_file = open("./static/assets/plot.png", "wb")
    image_file.write(base64.b64decode((data_image)))
    image_file.close()
