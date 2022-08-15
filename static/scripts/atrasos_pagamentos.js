$(document).ready(function () {
    $(".analise-selecionada").change(function () {
        var analise_selecionada = $('input[name="analise"]:checked').val();

        if (analise_selecionada == "Análise de não Conformidade") {
            $('input:radio[name="limite-empenho"]:first').click();
        }

        $("#analise-forms .row:last").toggle(speed = "fast", easing = "linear");
    });

    $(".limite-selecionado").change(function () {
        var limite = $('input[name="limite-empenho"]:checked').val();

        if (limite == "Não aplicado") {
            $("input#valor-limite").attr("disabled", true);
            $("input#valor-limite").removeAttr("required");
            $("input#valor-limite").val("");
        } else {
            $("input#valor-limite").removeAttr("disabled");
            $("input#valor-limite").attr("required", true);
        }

        $("#valor-limite").attr("placeholder", limite);
    });
});