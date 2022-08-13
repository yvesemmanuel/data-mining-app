from flask import Flask, render_template, request
import pandas as pd
import json

from static.scripts.MontaSagresSimba import *
from static.scripts.Getters import *
from static.scripts.Plots import *

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/analises/atraso_pagamentos", methods=["GET", "POST"])
def atraso_pagamentos():
    anos = ["2020"]
    cores = ["Pior UO+FONTE", "Média UO+FONTE"]
    entidades = ["Pessoa Física", "Pessoa Jurídica", "Ambos"]
    # limites = ["Não aplicado", "Menor que", "Maior que"]

    municipios = list(
        pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";").Municipio
    )

    if request.method == "POST":
        cor_mapa, ano = request.form.get("cormapa"), request.form.get("ano")
        analise = request.form.get("analise")

        if cor_mapa == "Pior UO+FONTE":
            mapa_selecionado = "mapa_pior"
        elif cor_mapa == "Média UO+FONTE":
            mapa_selecionado = "mapa_media"

        limite_empenho = request.form.get("limite-empenho")
        if analise == "Análise de Atrasos":
            entidade = request.form.get("entidade")
            limite_empenho = request.form.get("limite-empenho")
            valor_limite = request.form.get("valor-limite")

            return render_template(
                "atraso_pagamentos.html",
                title="Análise de Atraso de Pagamentos",
                method=request.method,
                anos=anos,
                cores=cores,
                entidades=entidades,
                mapa=mapa_selecionado,
                cor_selecionada=cor_mapa,
                analise_selecionada=analise,
                entidade_selecionada=entidade,
                limite_selecionado=limite_empenho,
                valor_selecionado=valor_limite,
                municipios=municipios
            )
        elif analise == "Análise de não Conformidade":
            return render_template(
                "atraso_pagamentos.html",
                title="Análise de Atraso de Pagamentos",
                method=request.method,
                anos=anos,
                cores=cores,
                entidades=entidades,
                mapa=mapa_selecionado,
                cor_selecionada=cor_mapa,
                analise_selecionada=analise,
                municipios=municipios
            )

    return render_template(
        "atraso_pagamentos.html",
        title="Análise de Atraso de Pagamentos",
        anos=anos,
        method=request.method,
        cores=cores,
        entidades=entidades
    )


@app.route("/mapa_pior")
def mapa_pior():
    return render_template("mapa_pior.html")


@app.route("/mapa_media")
def mapa_media():
    return render_template("mapa_media.html")


@app.route("/analises/pagamentos_regulares", methods=["GET", "POST"])
def pag_reg():
    municipios = list(
        pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";").Municipio
    )

    if request.method == "POST":
        municipio = request.form.get("municipio")

        # pegando os empenhos associados ao municipio
        empenhos = get_salario_emp(municipio)
        lista_empenhos = []
        for idx, empenho in enumerate(empenhos):
            lista_empenhos.append(str(idx) + " - " + str(empenho.nmFornecedor))

        if request.form.get("action") == "aplicar":
            empenho = empenhos[0]
            criar_plot_1(empenho)
        elif request.form.get("action") == "atualizar":
            num_empenho = int(request.form.get("empenho").split(" - ")[0])
            empenho = empenhos[num_empenho]
            criar_plot_1(empenho)

        # informações do empenho
        cpf_cnpj = "{} ({})".format(empenho.cnpj, empenho.nmFornecedor)

        lista_datas = map(date_to_string, empenho.datasPagamentosDateTime)
        datas = "; ".join(lista_datas)

        lista_valores = map(str, empenho.listValoresPagamentos)
        valores = "; ".join(lista_valores)

        descricao = empenho.descricao

        info = {
            "cpf_cnpj": cpf_cnpj,
            "datas": datas,
            "valores": valores,
            "descricao": descricao,
        }

        return render_template(
            "pagamentos_regulares.html",
            title="Análise de Pagamentos Regulares",
            municipios=municipios,
            method=request.method,
            municipio_selecionado=municipio,
            empenho_selecionado=request.form.get("empenho"),
            lista_empenhos=lista_empenhos,
            info_empenho=info,
        )

    return render_template(
        "pagamentos_regulares.html",
        title="Análise de Pagamentos Regulares",
        municipios=municipios,
        method=request.method,
    )


def date_to_string(date):
    return date.strftime("%d/%m/%Y")


@app.route("/analises/servicos_antes_empenho", methods=["GET", "POST"])
def servicos_antes():
    municipios = list(
        pd.read_csv("./static/datasets/ListaMunicipios.csv", sep=";").Municipio
    )

    if request.method == "POST":
        municipio = request.form.get("municipio")

        empenhos = get_servico_emp(municipio)
        lista_empenhos = []
        for idx, empenho in enumerate(empenhos):
            lista_empenhos.append(str(idx) + " - " + str(empenho.nmFornecedor))

        if request.form.get("action") == "aplicar":
            empenho = empenhos[0]
            criar_plot_2(empenho)
        elif request.form.get("action") == "atualizar":
            num_empenho = int(request.form.get("empenho").split(" - ")[0])
            empenho = empenhos[num_empenho]
            criar_plot_2(empenho)

        cpf_cnpj = "{} ({})".format(empenho.cnpj, empenho.nmFornecedor)
        primeiro_mes = str(round(empenho.vlMes1, 2))
        media_mensal = str(round(empenho.vlMedioMensal, 2))

        lista_datas = map(date_to_string, empenho.datasPagamentosDateTime)
        datas = "; ".join(lista_datas)

        lista_valores = map(str, empenho.listValoresPagamentos)
        valores = "; ".join(lista_valores)

        descricao = empenho.descricao

        info = {
            "cpf_cnpj": cpf_cnpj,
            "datas": datas,
            "valores": valores,
            "descricao": descricao,
            "primeiro_mes": primeiro_mes,
            "media_mensal": media_mensal,
        }

        return render_template(
            "servicos_antes.html",
            title="Análise de Serviços Antes de Empenho",
            municipios=municipios,
            method=request.method,
            municipio_selecionado=municipio,
            empenho_selecionado=request.form.get("empenho"),
            lista_empenhos=lista_empenhos,
            info_empenho=info,
        )

    return render_template(
        "servicos_antes.html",
        title="Análise de Serviços Antes de Empenho",
        municipios=municipios,
        method=request.method,
    )


@app.route("/analises/simba", methods=["GET", "POST"])
def simba():
    lObjs = montaObjsSagresSimba(
        "simba/SimbaGoiana.csv", "simba/SagresGoiana.csv")
    lst_idx_simba_sagres = []
    for idx, o in enumerate(lObjs):
        lst_idx_simba_sagres.append(
            "{} - {}({}) - {}".format(
                idx, o.nmFornecedor, o.cpf_cnpj, round(
                    o.somaSimba - o.somaSagres, 2)
            )
        )

    meses = [
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

    if request.method == "POST":
        entidade_idx = int(request.form.get("entidade").split(" - ")[0])
        entidade = lObjs[entidade_idx]

        dictPagsSagres = entidade.dictPagsMensaisSagres
        dictPagsSimba = entidade.dictPagsMensaisSimba

        linhaSagres = []
        linhaSimba = []

        for idx in range(1, 13):
            linhaSagres.append(round(dictPagsSagres[idx], 2))
            linhaSimba.append(round(dictPagsSimba[idx], 2))

        info = {"fornecedor": entidade.nmFornecedor}
        criar_plot_3(entidade_idx)

        tb_info = {"meses": meses, "sagres": linhaSagres, "simba": linhaSimba}

        return render_template(
            "simba.html",
            title="SIMBA",
            indexes=lst_idx_simba_sagres,
            info_entidade=info,
            table_info=tb_info,
            idx_selecionado=request.form.get("entidade"),
        )

    entidade_idx = 0
    entidade = lObjs[entidade_idx]

    dictPagsSagres = entidade.dictPagsMensaisSagres
    dictPagsSimba = entidade.dictPagsMensaisSimba

    linhaSagres = []
    linhaSimba = []

    for idx in range(1, 13):
        linhaSagres.append(round(dictPagsSagres[idx], 2))
        linhaSimba.append(round(dictPagsSimba[idx], 2))

    info = {"fornecedor": entidade.nmFornecedor}
    criar_plot_3(entidade_idx)

    tb_info = {"meses": meses, "sagres": linhaSagres, "simba": linhaSimba}

    return render_template(
        "simba.html",
        title="SIMBA",
        indexes=lst_idx_simba_sagres,
        info_entidade=info,
        table_info=tb_info,
        idx_selecionado=request.form.get("entidade"),
    )


@app.route("/analises/correspondencia_fontes", methods=["GET", "POST"])
def correspondencia_fontes():
    municipios = ["Cabo de Santo Agostinho"]

    if request.method == "POST":
        municipio_selecionado = request.form.get("municipio")

        colunas, linhas, linhas_descricoes, descricao_geral = get_dados_correspondencia(
            municipio_selecionado)

        return render_template("correspondencia_fontes.html", title="Correspondência Entre Fontes de Dados", municipios=municipios, method=request.method, municipio_selecionado=municipio_selecionado, colunas=colunas, linhas=linhas, linhas_descricoes=json.dumps(linhas_descricoes), descricao_geral=descricao_geral)

    return render_template("correspondencia_fontes.html", title="Correspondência Entre Fontes de Dados", municipios=municipios, method=request.method)


if __name__ == "__main__":

    app.run(debug=True)
