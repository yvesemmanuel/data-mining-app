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
            $("#valor-limite").attr("disabled", "");
            $("input#valor-limite").val("");
        } else {
            $("#valor-limite").removeAttr("disabled");
        }

        $("#valor-limite").attr("placeholder", limite);
    });
});