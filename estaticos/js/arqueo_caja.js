updateSubs();

var cant_efectivo_manual = $('.cant_efectivo_manual'),
sub_otros_manual = $('.sub_otros_manual');

cant_efectivo_manual.keyup(updateSubs);
sub_otros_manual.keyup(updateTotal);

$('.sub_valor_manual').each(function() {
    new MutationObserver(updateTotal).observe(this, {childList: true, subtree: true});
});

function updateSubs() {
    $('#efectivo_1').text($('#id_mil').val() * 1000);
    $('#efectivo_2').text($('#id_quinientos').val() * 500);
    $('#efectivo_3').text($('#id_doscientos').val() * 200);
    $('#efectivo_4').text($('#id_cien').val() * 100);
    $('#efectivo_5').text($('#id_b_cincuenta').val() * 50);
    $('#efectivo_6').text($('#id_veinte').val() * 20);
    $('#efectivo_7').text($('#id_diez').val() * 10);
    $('#efectivo_8').text($('#id_cinco').val() * 5);
    $('#efectivo_9').text($('#id_m_dos').val() * 2);
    $('#efectivo_10').text($('#id_uno').val() * 1);
    $('#efectivo_11').text($('#id_m_cincuenta').val() * 0.50);
    $('#efectivo_12').text($('#id_veinticinco').val() * 0.25);
    updateTotal();
}

function updateTotal() {
    var sum = 0;
    $('.sub_valor_manual').each(function() {
        sum += +$(this).text();
    });
    $('.sub_otros_manual').each(function() {
        sum += +$(this).val();
    });
    $('.sub_manual').val(sum);
}