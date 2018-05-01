Habilitación de Criadero de Cerdos
==================================
  Se presentará una pantalla que contendrá un listado con todas las *Habilitaciones de Criadero*
  que se encuentren registradas en el sistema hasta la fecha.

  .. image:: _static/listado_habilitacion.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Habilitación*.

  Estas funcionalidades son:

    - :ref:`Detalle Habilitación <detalle-habilitacion>`
    - :ref:`Eliminar habilitación <eliminar-habilitacion>`
    - :ref:`Aplazar habilitación <aplazar-habilitacion>`
    - :ref:`Registrar Disposición <registrar-disposicion>`

  Además, si el usuario desea Registrar una nueva *Habilitación*:

    - :ref:`Nueva Solicitud de Habilitación de Criadero de Cerdos <nueva-habilitacion>`


.. _nueva-habilitacion:

Nueva Solicitud de Habilitación de Criadero de Cerdos
-----------------------------------------------------

  Si el usuario desea crear una nueva *Habilitación*, deberá presionar el botón ``Nueva Solicitud``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/nueva_habilitacion.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Habilitación*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de las habilitaciones.


.. _detalle-habilitacion:

Detalle habilitación
--------------------

  Si el usuario desea ver el detalle de una *Habilitación*, deberá seleccionar en la columna de **acciones** asociado a la *Habilitación* y presionar el ícono ``Detalle``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/detalle_habilitacion.png
    :align: center

  En esta parte el usuario podrá observar la información adicional de la *Habilitación*. Si desea imprimir el detalle, deberá presionar el botón ``Imprimir``, de otro modo, si desea volver al listado inicial, presionará el botón ``Regresar``.


.. _eliminar-habilitacion:


Eliminar habilitación
---------------------

   Si el usuario desea eliminar una *Habilitación*, deberá seleccionar en la columna de **acciones** asociado a la *Habilitación* y presionar el ícono ``Eliminar``

   Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

   .. image:: _static/baja_habilitacion.png
     :align: center

   En esta parte el usuario deberá decidir si confirma la eliminación de la *Habilitación* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _aplazar-habilitacion:

Aplazar Habilitación
--------------------

  Si el usuario desea aplazar una nueva *Habilitación*, deberá seleccionar en la columna de **acciones** asociado a la *Habilitación* y presionar el ícono ``Aplazar``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/aplazar_habilitacion.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los motivos por la cual se aplaza la *Habilitación*.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado con todas las habilitaciones.


.. _registrar-disposicion:

Registrar Disposición
---------------------

  Si el usuario desea ver registrar una *Disposición*, deberá seleccionar en la columna de **acciones** asociado a la *Habilitación* y presionar el ícono ``Registrar disposición``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/registrar_disposicion.png
    :align: center

  En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Habilitación*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Habilitación* seleccionada, caso contrario, presionará el botón ``Cancelar``..
