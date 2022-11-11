from matplotlib.figure import Figure
import numpy as np
from statistics import mean, stdev
# from scripts.MontaSagresSimba import *
import plotly.express as px


def regular_payments_plot(x, y):
    fig = Figure(figsize=(5,3))
    ax = fig.subplots()

    ax.plot(x, y, color='black', linestyle='--', marker='o')

    avg = mean(y)
    std = stdev(y)
    lb = []
    up = []
    for i in range(len(y)):
        lb.append(avg - std)
        up.append(avg + std)

    ax.fill_between(x, lb, up, alpha=0.2)
    fig.autofmt_xdate()

    ax.set_xlabel('Data Pagamento')
    ax.set_ylabel('Valor (R$)')

    return fig


def service_before_payment_plot(x, y):
    fig = Figure(figsize=(5,3))
    ax = fig.subplots()

    ax.plot(x, y, color='black', linestyle='--', marker='o')
    fig.set_size_inches(7.41, 5)

    avg = mean(y)
    std = stdev(y)

    lb = []
    ub = []
    for _ in range(len(y)):
        lb.append(avg - std)
        ub.append(avg + std)

    ax.fill_between(x, lb, ub, alpha=0.2)
    fig.autofmt_xdate()

    ax.set_xlabel('Data Pagamento')
    ax.set_ylabel('Valor (R$)')

    return fig


def simba_plot(y0, y1, supplier):
    fig = Figure(figsize=(8, 5))
    ax = fig.subplots()

    barWidth = 0.25
    r1 = np.arange(12)
    r2 = [x + barWidth for x in r1]

    ax.bar(r1, y0, color='#6A5ACD', width=barWidth, label='Sagres')
    ax.bar(r2, y1, color='#00BFFF', width=barWidth, label='Simba')

    ax.ticklabel_format(style='plain')
    ax.set(
        title='Destino: ' + supplier,
        xlabel='Mês',
        ylabel='Valor Mensal (R$)',
    )
    ax.set_xticklabels(
        [
            'Jan',
            'Fev',
            'Mar',
            'Abr',
            'Mai',
            'Jun',
            'Jul',
            'Ago',
            'Set',
            'Out',
            'Nov',
            'Dez',
        ]
    )
    ax.set_xticks([r + barWidth for r in range(12)])
    ax.legend(loc='upper right')

    fig.autofmt_xdate()

    return fig

def payments_delay_plot_0(x):
    # fig = Figure()
    fig = Figure(figsize=(5,3))
    ax = fig.subplots()

    b = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    # n, bins, patches = ax.hist(x, bins=b)
    # ax.grid(color='white', lw=4.5, axis='x')

    # xticks = [(bins[idx + 1] + value) / 2 for idx,
    #           value in enumerate(bins[:-1])]
    # xticks_labels = ['{:.2f}\nto\n{:.2f}'.format(value, bins[idx + 1]) for idx, value in enumerate(bins[:-1])]
    # plt.xticks(xticks, labels = xticks_labels)

    # for idx, value in enumerate(n):
    #     if value > 0:
    #         ax.text(xticks[idx], value + 5, int(value), ha='center')

    ax.set_xticks(b)

    return fig


def payments_delay_plot_1(df):
    fig = px.scatter(df, x='ATRASO', y='VALOR', color='FORNECEDOR')

    fig.write_html('./templates/payments_delay_plot_1.html')
    HtmlFile = open('./templates/payments_delay_plot_1.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    
    return source_code