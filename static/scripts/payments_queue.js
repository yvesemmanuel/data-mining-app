$(document).ready(function () {
    $(".correspondencia-table").dataTable({
        searching: false, info: false,
        bLengthChange: false,
        language: {
            paginate: {
                previous: "Anterior",
                next: "Próximo"
            }
        },
        rowReorder: true,
        columnDefs: [
            { orderable: true, className: 'reorder', targets: [0, 3] },
            { orderable: false, targets: '_all' }
        ]
    });

    $(".fila-table").dataTable({
        searching: false, info: false,
        bLengthChange: false,
        language: {
            paginate: {
                previous: "Anterior",
                next: "Próximo"
            }
        },
        rowReorder: true,
        columnDefs: [
            { orderable: true, className: 'reorder', targets: [2, 3, 4, 5, 6] },
            { orderable: false, targets: '_all' }
        ]
    });

});