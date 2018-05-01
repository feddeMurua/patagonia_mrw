Libretas Sanitarias
===================
  Se presentará una pantalla que contendrá un listado con todas las *Libretas Sanitarias*
  que se encuentren registradas en el sistema hasta la fecha.

  .. image:: _static/listado_libreta.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Libreta*.

  Estas funcionalidades son:

    - :ref:`Modificar Libreta <modificar-libreta>`
    - :ref:`Eliminar Libreta <eliminar-libreta>`
    - :ref:`Detalle Libreta <detalle-libreta>`
    - :ref:`Renovación Libreta <renovacion-libreta>`

  Además, si el usuario desea Registrar una nueva *Libreta*:

    - :ref:`Nueva Libreta <nueva-libreta>`


.. _nueva-libreta:

Nueva Libreta
-------------

  Si el usuario desea crear una nueva *Libreta*, deberá presionar el botón ``Nueva Libreta``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_libreta.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Libreta*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de las libretas.

.. _modificar-libreta:

Modificación de Libreta
-----------------------

   Si el usuario desea modificar los datos de una *Libreta*, deberá seleccionar en la columna de **acciones** asociado a la *Libreta* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image:: _static/mod_libreta.png
     :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Libreta*.

   .. ATTENTION::
       El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
       En este punto, las posibles causas de errores son:

           - Uno o más campos obligatorios vacíos.
           - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Libreta* seleccionada, caso contrario, presionará el botón ``Cancelar``.

.. _eliminar-libreta:


Eliminar Libreta
----------------

   Si el usuario desea eliminar una *Libreta*, deberá seleccionar en la columna de **acciones** asociado a la *Libreta* y presionar el ícono ``Eliminar``

   Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

   .. image:: _static/baja_libreta.png
     :align: center

   En esta parte el usuario deberá decidir si confirma la eliminación de la *Libreta* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _detalle-libreta:

Detalle Libreta
---------------

  Si el usuario desea ver el detalle de una *Libreta*, deberá seleccionar en la columna de **acciones** asociado a la *Libreta* y presionar el ícono ``Detalle``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/detalle_libreta.png
    :align: center

  En esta parte el usuario podrá observar la información adicional de la *Libreta*. Si desea imprimir la tarjeta, deberá presionar el botón ``Imprimir Tarjeta``, de otro modo, si desea volver al listado inicial, presionará el botón ``Regresar``.


.. _renovacion-libreta:

Renovación Libreta
------------------

  Si el usuario desea ver renovar una *Libreta*, deberá seleccionar en la columna de **acciones** asociado a la *Libreta* y presionar el ícono ``Renovación``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/renovacion_libreta.png
    :align: center

  En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Libreta*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Libreta* seleccionada, caso contrario, presionará el botón ``Cancelar``..
