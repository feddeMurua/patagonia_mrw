var sum_sis = 0;
$('.sub_valor_sistema').each(function() {
    sum_sis += +($(this).text());
});
$('.sub_sistema').text(sum_sis);

updateSubs();

var cant_efectivo_manual = $('.cant_efectivo_manual'),
sub_otros_manual = $('.sub_otros_manual');

cant_efectivo_manual.keyup(updateSubs);
sub_otros_manual.keyup(updateTotal);

$('.sub_valor_manual').each(function() {
    new MutationObserver(updateTotal).observe(this, {childList: true, subtree: true});
});

function updateSubs() {
    $('#efectivo_1').text($('#id_billetes_quinientos').val() * 500);
    $('#efectivo_2').text($('#id_billetes_doscientos').val() * 200);
    $('#efectivo_3').text($('#id_billetes_cien').val() * 100);
    $('#efectivo_4').text($('#id_billetes_cincuenta').val() * 50);
    $('#efectivo_5').text($('#id_billetes_veinte').val() * 20);
    $('#efectivo_6').text($('#id_billetes_diez').val() * 10);
    $('#efectivo_7').text($('#id_billetes_cinco').val() * 5);
    $('#efectivo_8').text($('#id_billetes_dos').val() * 2);
    $('#efectivo_9').text($('#id_monedas_dos').val() * 2);
    $('#efectivo_10').text($('#id_monedas_uno').val() * 1);
    $('#efectivo_11').text($('#id_monedas_cincuenta').val() * 0.5);
    $('#efectivo_12').text($('#id_monedas_veinticinco').val() * 0.25);
    updateTotal();
}

function updateTotal() {
    var sum = 0;
    $('.sub_valor_manual').each(function() {
        sum += +($(this).text());
    });
    $('.sub_otros_manual').each(function() {
        sum += +($(this).val());
    });
    $('.sub_manual').text(sum);
}