Controles
=========
  Se presentará una pantalla que contendrá un listado con todos los *Controles*
  que se encuentren registrados en el sistema hasta la fecha.

  .. image:: _static/listado_control_plaga.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Control de Plaga*.

  Estas funcionalidades son:

   - :ref:`Visita control de plagas <visita-control>`
   - :ref:`Detalle control de plagas <detalle-control>`
   - :ref:`Modificar control de plagas <modificar-control>`
   - :ref:`Eliminar control de plagas <eliminar-controlplaga>`
   - :ref:`Pagar control de plagas <pagar-control>`

   Además, si el usuario desea Registrar un nuevo *Control*:

   - :ref:`Nuevo Control <alta-control>`


.. _alta-control:

Nuevo Control
-------------

  Si el usuario desea crear un nuevo *Control de Plaga*, deberá presionar el botón ``Nuevo Control``.

  A continuación, el sistema lo redirigirá a la siguiente pantalla. En esta parte, al usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Control de Plaga*.

  .. image:: _static/alta_control_plaga.png
     :align: center

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de vehículos.


.. _visita-control:

Visita Control de Plagas
------------------------

   Si el usuario desea registrar la visita de un control, deberá seleccionar en la columna de **acciones** asociado al *control* y
   presionar el ícono ``Visitas``.

   En esta parte al usuario se le presentará un listado con todas las visitas asociadas al *Control de plagas*.

   .. toctree::
      :maxdepth: 1

      visitacontrolplaga


.. _detalle-control:

Detalle del Control de plagas
-----------------------------

   Si el usuario desea ver el detalle de un *Control*, deberá seleccionar en la columna de **acciones** asociado al *Control* y
   presionar el ícono ``Detalle``.

   Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

   .. image:: _static/detalle_control_plagas.png
      :align: center

   En esta parte el usuario podrá observar la información adicional del *Control*.


.. _modificar-control:

Modificar control de plagas
---------------------------

   Si el usuario desea modificar los datos de un *control*, deberá seleccionar en la columna de **acciones** asociado al *control* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image:: _static/mod_control_plagas.png
      :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados al *control*.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos del *control* seleccionado.


.. _eliminar-controlplaga:

Eliminar Control de Plagas
--------------------------

 Si el usuario desea eliminar un *Control de plagas*, deberá seleccionar en la columna de **acciones** asociado al *control* y presionar el ícono ``Eliminar``

 Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

 .. image:: _static/baja_control_plaga.png
    :align: center

 En esta parte el usuario deberá decidir si confirma la eliminación del *control* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _pagar-control:

Pagar Control de Plagas
--------------------------

  Si el usuario desea registrar el pago de un *Control de plagas*, deberá seleccionar en la columna de **acciones** asociado al *control* y presionar el ícono ``Pagar``.

  Una vez realizado el paso anterior aparecerá el siguiente formulario:

  .. image:: _static/pagar_controlplaga.png
     :align: center

  Como procedimiento final, el usuario deberá decidir si se trata de una factura previa o una nueva y confirmar la operación presionando el botón ``Aceptar``, caso contrario, presionará el botón ``Cancelar``.
