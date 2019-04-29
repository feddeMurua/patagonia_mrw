Esterilización
==============
Se presentará una pantalla que contendrá un listado con todos las *Esterilizaciones*
que se encuentren registradas en el sistema hasta la fecha.

.. image:: _static/listado_esterilizaciones.png
    :align: center

Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Esterilización*.

Estas funcionalidades son:

- :ref:`Imprimir Consentimiento <imprimir-esterilizacion>`
- :ref:`Eliminar Esterilización <eliminar-esterilizacion>`
- :ref:`Confirmar Esterilización <confirmar-esterilizacion>`

Además, si el usuario desea Registrar un nuevo *Turno*:

- :ref:`Nuevo Turno - Mascota patentada <nuevo-turno_p>`
- :ref:`Nuevo Turno - Mascota No patentada <nuevo-turno_np>`


.. _nuevo-turno_p:

Nuevo Turno - Mascota patentada
-------------------------------

  Si el usuario desea crear un nuevo *Turno* de una mascota patentada, deberá presionar el botón ``Nuevo Turno - Mascota patentada``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_esterilizacion.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Turno*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de esterilizaciones.


.. _nuevo-turno_np:

Nuevo Turno - Mascota No patentada
----------------------------------

  Si el usuario desea crear un nuevo *Turno* de una mascota ``No`` patentada, deberá presionar el botón ``Nuevo Turno - Mascota No patentada``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_esterilizacion_no_p.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Turno*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de esterilizaciones.


.. _imprimir-esterilizacion:

Imprimir Consentimiento
-----------------------

  Si el usuario desea imprimir el consentimiento informado para cirguía deberá seleccionar en la columna de **acciones** asociado a la *Esterilización* y presionar el ícono ``Imprimir Consentimiento``.
  A continuación, el sistema abrirá en una pestaña emergente, el formulario en formato ".pdf" para imprimir.


.. _eliminar-esterilizacion:

Eliminar Esterilización
-----------------------

  Si el usuario desea eliminar una *Esterilización*, deberá seleccionar en la columna de **acciones** asociado a la *Esterilización* y presionar el ícono ``Eliminar``.

  Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

  .. image:: _static/baja_esterilizacion.png
    :align: center

  En esta parte el usuario deberá decidir si confirma la eliminación del *Turno* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _confirmar-esterilizacion:

Confirmar Esterilización
------------------------

  Si el usuario desea confirmar una *Esterilización*, deberá seleccionar en la columna de **acciones** asociado a la *Esterilización* y presionar el ícono ``Confirmar realización``.

  Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

  .. image:: _static/confirmar_esterilizacion.png
    :align: center

  En esta parte el usuario deberá decidir si confirma la esterilización o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.
