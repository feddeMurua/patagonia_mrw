Análisis de Triquinosis
=======================
  Se presentará una pantalla que contendrá un listado con todos los *Análisis*
  que se encuentren registrados en el sistema hasta la fecha.

  .. image:: _static/listado_analisis.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Análisis*.

  Estas funcionalidades son:

    - :ref:`Detalle Análisis <detalle-analisis>`
    - :ref:`Eliminar Análisis <eliminar-Análisis>`
    - :ref:`Modificar Análisis <modificar-Análisis>`
    - :ref:`Registrar Resultado del Análisis <registrar-resultado>`

  Además, si el usuario desea dar de alta un nuevo *Análisis*:

    - :ref:`Nuevo Análisis <nuevo-Análisis>`


.. _nuevo-Análisis:

Nuevo Análisis
--------------

  Si el usuario desea crear un nuevo *Análisis*, deberá presionar el botón ``Nuevo Análisis``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_analisis.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Análisis*.

  .. ATTENTION::
      Se puede observar un botón verde con la leyenda ``Agregar`` en el campo *Procedencia*, el cual es utilizado para
      agregar una nueva procedencia (localidad) respectivamente si no se encuentra registrada en el sistema. Además;
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de Análisis.


.. _detalle-analisis:

Detalle Análisis
----------------

  Si el usuario desea ver el detalle de un *Análisis*, deberá seleccionar en la columna de **acciones** asociado al *Análisis* y presionar el ícono ``Detalle``

  Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

  .. image:: _static/detalle_analisis.png
    :align: center

  En esta parte el usuario podrá observar la información adicional del *Análisis*. Si desea imprimir el comprobante, deberá presionar el botón ``Imprimir Comprobante``, de otro modo, si desea volver al listado inicial, presionará el botón ``Regresar``.


.. _eliminar-Análisis:

Eliminar Análisis
-----------------

  Si el usuario desea eliminar un *Análisis*, deberá seleccionar en la columna de **acciones** asociado al *Análisis* y presionar el ícono ``Eliminar``

  Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

  .. image:: _static/baja_analisis.png
    :align: center

  En esta parte el usuario deberá decidir si confirma la eliminación del *Análisis* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _modificar-Análisis:

Modificación de Análisis
------------------------

  Si el usuario desea modificar los datos de un *Análisis*, deberá seleccionar en la columna de **acciones** asociado al *Análisis* y presionar el ícono ``Modificar``.

  Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/mod_analisis.png
    :align: center

  En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados al *Análisis*.

  .. ATTENTION::

      Se puede observar un botón verde con la leyenda ``Agregar`` en el campo *Procedencia*, el cual es utilizado para
      agregar una nueva procedencia (localidad) respectivamente si no se encuentra registrada en el sistema. Además;
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos del *Análisis* seleccionado.


.. _registrar-resultado:

Registrar Resultado del Análisis
--------------------------------

  Si el usuario desea registrar un resultado de un *Análisis*, deberá seleccionar en la columna de **acciones** asociado al *Análisis* y presionar el ícono ``Registrar resultado``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/registrar_resultado_analisis.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para registrar el resultado del *Análisis*.
