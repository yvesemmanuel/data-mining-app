$(document).ready(function () {
    $(".analysis-selected").change(function () {
        var selected_analysis = $('input[name="analysis"]:checked').val();

        if (selected_analysis == "Análise de não Conformidade") {
            $('input:radio[name="selected_limit-empenho"]:first').click();
        }

        $("#analysis-form .row:last").toggle(speed = "fast", easing = "linear");
    });

    $(".limit-options").change(function () {
        var selected_limit = $('input[name="loan-limit"]:checked').val();

        if (selected_limit == "Não aplicado") {
            $("input#loan-value").attr("disabled", true);
            $("input#loan-value").removeAttr("required");
            $("input#loan-value").val("");
        } else {
            $("input#loan-value").removeAttr("disabled");
            $("input#loan-value").attr("required", true);
        }

        $("#loan-value").attr("placeholder", selected_limit);
    });
});