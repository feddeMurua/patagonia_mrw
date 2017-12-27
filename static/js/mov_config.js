var forma_pago = $('#id_forma_pago'),
nro_cheque = $('#id_nro_cheque');
forma_pago.on('change', hideNroCheque);
hideNroCheque();

function hideNroCheque() {
    if (forma_pago.val() == 'Cheque') {
        nro_cheque.parent().removeClass('hidden');
        nro_cheque.prop('required', true);
    } else {
        nro_cheque.parent().addClass('hidden');
        nro_cheque.prop('required', false);
    }
}