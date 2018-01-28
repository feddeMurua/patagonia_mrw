var previa = $('.previa'),
nueva = $('.nueva')
movimiento = $('#id_movimiento'),
titular = $('#id_titular'),
nro_ingreso = $('#id_nro_ingreso'),
forma_pago = $('#id_forma_pago'),
nro_cheque = $('#id_nro_cheque');

forma_pago.on('change', hideNroCheque);
hideNroCheque();

tipo_factura = $("input[name='optradio']:checked").val();
hideFields();

$('#radio_options').change(function(){
    tipo_factura = $("input[name='optradio']:checked").val();
    hideFields();
});

function hideFields() {
    if (tipo_factura == 'previa') {
        movimiento.prop('required', true);
        titular.prop('required', false);
        nro_ingreso.prop('required', false);
        forma_pago.prop('required', false);
        nro_cheque.prop('required', false);
        previa.removeClass('hidden');
        nueva.addClass('hidden');
    } else {
        movimiento.prop('required', false);
        titular.prop('required', true);
        nro_ingreso.prop('required', true);
        forma_pago.prop('required', true);
        nueva.removeClass('hidden');
        previa.addClass('hidden');
    }
}

function hideNroCheque() {
    if (forma_pago.val() == 'Cheque') {
        nro_cheque.parent().removeClass('hidden');
        nro_cheque.prop('required', true);
    } else {
        nro_cheque.parent().addClass('hidden');
        nro_cheque.prop('required', false);
    }
}

function requireNone() {
    movimiento.prop('required', false);
    titular.prop('required', false);
    nro_ingreso.prop('required', false);
    forma_pago.prop('required', false);
    nro_cheque.prop('required', false);
}