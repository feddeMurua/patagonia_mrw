Patentamiento de Mascotas
=========================

  Se presentará una pantalla que contendrá un listado con todas las *Patentes*
  que se encuentren registradas en el sistema hasta la fecha.

  .. image:: _static/listado_patentes.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Patente*.

  Estas funcionalidades son:

    - :ref:`Imprimir Carnet <imprimir-carnet>`
    - :ref:`Retiro de Beneficios <retiro-beneficios>`
    - :ref:`Detalle Patente <detalle-patente>`
    - :ref:`Modificar Patente <modificar-patente>`
    - :ref:`Eliminar Patente <eliminar-patente>`
    - :ref:`Renovación Patente <renovacion-patente>`

  Además, si el usuario desea Registrar una nueva *Patente*:

    - :ref:`Nueva Patente <nueva-patente>`


.. _nueva-patente:

Nueva Patente
-------------

  Si el usuario desea crear una nueva *Patente*, deberá presionar el botón ``Nueva Patente``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_patente.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Patente*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de las Patentes.


.. _imprimir-carnet:

Imprimir Carnet
---------------

<<<<<<< HEAD
Si el usuario desea imprimir el *Carnet* correspondiente a la *Mascota* patentada, debera presionar el ícono ``Confirmar`` asociado a la *Patente* en la columna de **acciones**.
=======
  Si el usuario desea imprimir un *Carnet*, deberá seleccionar en la columna de **acciones** asociado a la *Patente* y presionar el ícono ``Imprimir Carnet``.

  A continuación, el sistema presentará en una nueva pestaña un archivo en formato .PDF para imprimir el carnet correspondiente a la patente.
>>>>>>> cd755d2912d003dbc86232a49a11a5ead353f9b9


.. _retiro-beneficios:

Retiro de Beneficios
--------------------

  Si el usuario desea registrar un nuevo retiro de un *Garrapaticida* o *Atiparasitario*, deberá presionar el ícono ``Retiro de beneficios`` asociado a la *Patente* en la columna de **acciones**. Acto seguido, se abrirá la siguiente vista emergente:

  .. image:: _static/retiro_beneficios.png
    :align: center

  En esta ventana el usuario deberá seleccionar el tipo de beneficio que desea retirar. Para cerrar la ventana en caso de no seleccionar una opción, el usuario debera presionar el botón ``X`` en la esquina superior derecha, o bin hacer click en cualquier otro lugar de la pantalla.

  Una vez seleccionado un beneficio, se abrirá una nueva vista emergente, informando si el retiro se realizó con exito, o si por el contrario, existió algun error.


.. _detalle-patente:

Detalle de Patente
------------------

  Si el usuario desea ver el detalle de una *Patente*, deberá seleccionar en la columna de **acciones** asociado a la *Patente* y presionar el ícono ``Detalle``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/detalle_patente.png
    :align: center

  En esta parte el usuario podrá observar la información adicional de la *Patente*. Si desea imprimir la tarjeta, deberá presionar el botón ``Imprimir Tarjeta``, de otro modo, si desea volver al listado inicial, presionará el botón ``Regresar``.


.. _modificar-patente:

Modificación de Patente
-----------------------

   Si el usuario desea modificar los datos de una *Patente*, deberá seleccionar en la columna de **acciones** asociado a la *Patente* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image:: _static/mod_patente.png
     :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Patente*.

   .. ATTENTION::
       El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
       En este punto, las posibles causas de errores son:

           - Uno o más campos obligatorios vacíos.
           - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Patente* seleccionada, caso contrario, presionará el botón ``Cancelar``.


.. _eliminar-patente:


Eliminar Patente
----------------

   Si el usuario desea eliminar una *Patente*, deberá seleccionar en la columna de **acciones** asociado a la *Patente* y presionar el ícono ``Eliminar``

   Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

   .. image:: _static/baja_patente.png
     :align: center

   En esta parte el usuario deberá decidir si confirma la eliminación de la *Patente* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _renovacion-patente:

Renovación de Patente
---------------------

  Si el usuario desea ver renovar una *Patente*, deberá seleccionar en la columna de **acciones** asociado a la *Patente* y presionar el ícono ``Renovación Duplicado de Patente``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/renovacion_patente.png
    :align: center

  En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Patente*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Patente* seleccionada, caso contrario, presionará el botón ``Cancelar``.
