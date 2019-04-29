Cuentas Corrientes
==================
Se presentará una pantalla que contendrá un listado con todas las *Cuentas Corrientes* que se encuentren registradas en el sistema hasta la fecha.

.. image:: _static/listado_cc.png
     :align: center

Para ingresar al detalle de una *Cuenta Corriente*, el usuario deberá presionar el ícono ``Períodos`` en la columna de **acciones** asociado a la *Cuenta Corriente*. Al hacerlo, será redireccionado a la siguiente pantalla:
     
.. image:: _static/detalle_cc.png
     :align: center

En esta pantalla se mostrara el listado de todos los períodos de facturación de la *Cuenta Corriente*. Junto al listado, se presentará un conjunto de funcionalidades que permitirán interactuar con la *Cuenta Corriente*. Estas funcionalidades son:

  - :ref:`Detalle de período <detalle-periodo>`
  - :ref:`Generar certificado de deuda <certificado-deuda>`
  - :ref:`Abonar certificado de deuda <certificado-pago>`
  

.. _detalle-periodo:

Detalle de período
------------------
Si el usuario desea ingresar al detalle del período, deberá presionar el ícono ``Detalle de período`` en la columna de **acciones** asociado al *Período*. Al hacerlo será redireccionado a la siguiente pantalla:

.. image:: _static/detalle_periodo.png
     :align: center
     
En esta pantalla, se mostrará el listado de todas las reinspecciones que componen al *Período* seleccionado. Junto al listado, se presentará un conjunto de funcionalidades que permitirán interactuar con el *Período*. Estas funcionalidades son:

  - :ref:`Productos <productos-reinspeccion>`
  - :ref:`Eliminar <eliminar-reinspeccion>`
  

.. _productos-reinspeccion:

Productos
^^^^^^^^^
Si el usuario desea ver el el listado de productos de una *Reinspección*, deberá seleccionar en la columna de **acciones** asociado a la *Reinspección* y presionar el ícono ``Productos``

Una vez realizado el paso anterior, el usuario sera redirigido a la siguiente pantalla:

.. image:: _static/listado_productos_reinspeccion.png
     :align: center

En esta seccion, el usuario podrá verificar el listado de productos cargados en la *Reinspección*, modificar sus cantidades, o agregar productos faltantes.


.. _eliminar-reinspeccion:

Eliminar
^^^^^^^^
Si el usuario desea eliminar una *Reinspección*, deberá seleccionar en la columna de **acciones** asociado a la *Reinspección* y presionar el ícono ``Eliminar``

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/baja_reinspeccion.png
     :align: center

Aqui el usuario deberá decidir si confirma la eliminación de la *Reinspección* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _certificado-deuda:

Generar certificado de deuda
----------------------------
Si el usuario desea generar un *Certificado de Deuda*, deberá presionar el ícono ``Generar certificado de deuda`` en la columna de **acciones** asociada al *Período*. Al hacerlo sera redirigido a una nueva pantalla.

.. image:: _static/certificado_deuda.png
     :align: center

En esta pantalla el usuario podra visualizar la informacion correspondiente al *Abastecedor* y al *Período*, incluyendo un detalle de cada *Reinspección* que forme parte del detalle del *Período*.

Al presionar el botón ``Aceptar``, se generará un *Certificado de Deuda*, y se regresara al listado de períodos de la *Cuenta Corriente*.
     

.. _certificado-pdf:

Imprimir certificado de deuda
-----------------------------
Si el usuario desea imprimir un *Certificado de Deuda*, deberá presionar el ícono ``Imprimir certificado de deuda`` en la columna de **acciones** asociada al *Período*. Al hacerlo se abrira una nueva pestaña, en la que se podrá visualizar e imprimir el *Certificado de Deuda*.

.. _certificado-pago:

Abonar certificado de deuda
---------------------------
Si el usuario desea abonar *Certificado de Deuda* previamente generado, deberá presionar el ícono ``Abonar certificado de deuda`` en la columna de **acciones** asociada al *Período*. Al hacerlo sera redirigido a una nueva pantalla.

.. image:: _static/certificado_pago.png
     :align: center

En esta pantalla el usuario podra visualizar un resumen de la informacion correspondiente al *Certificado de Deuda*.
En caso de que exista una mora en el pago, se calculara automaticamente un interés, correspondiente a un 1% por cada dia de atraso luego de los 5 dias desde la generación del *Certificado de Deuda*. Se mostrará entonces el valor final con el interés incluido.

A continuación, se deberá ingresar los datos de facturación.

Una vez finalizado el proceso, se regresara al listado de períodos de la *Cuenta Corriente*.
