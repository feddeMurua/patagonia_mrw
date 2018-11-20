var previa = $('.previa'),
nueva = $('.nueva'),
movimiento = $('#id_movimiento'),
titular = $('#id_titular'),
forma_pago = $('#id_forma_pago'),
nro_cheque = $('#id_nro_cheque');

forma_pago.change(hideNroCheque);
hideNroCheque();

var tipo_factura = $("input[name='optradio']:checked").val();
hideFields();

$('#radio_options').change(function() {
    tipo_factura = $("input[name='optradio']:checked").val();
    hideFields();
});

function hideFields() {
    if (tipo_factura === 'previa') {
        $('.previa :input').prop('required', true);
        $('.nueva :input').prop('required', false);
        previa.removeClass('hidden');
        nueva.addClass('hidden');
    } else {
        $('.previa :input').prop('required', false);
        $('.nueva :input').prop('required', true);
        hideNroCheque();
        nueva.removeClass('hidden');
        previa.addClass('hidden');
    }
}

function hideNroCheque() {
    if (forma_pago.val() === 'Cheque') {
        nro_cheque.parent().removeClass('hidden');
        nro_cheque.prop('required', true);
    } else {
        nro_cheque.parent().addClass('hidden');
        nro_cheque.prop('required', false);
    }
}

function requireNone() {
    $('.previa :input').prop('required', false);
    $('.nueva :input').prop('required', false);
}