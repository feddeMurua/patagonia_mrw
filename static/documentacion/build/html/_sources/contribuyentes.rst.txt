Contribuyentes
==============
  Se presentará una pantalla que contendrá un listado con todos los *Contribuyentes*
  que se encuentren registrados en el sistema hasta la fecha.

  .. image:: _static/listado_contribuyentes.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Contribuyente*.

  Estas funcionalidades son:

   - :ref:`Detalle del Contribuyente <detalle-contribuyente>`
   - :ref:`Modificar Contribuyente <modificar-contribuyente>`
   - :ref:`Eliminar Contribuyente <eliminar-contribuyente>`

   Además, si el usuario desea Registrar un nuevo *Contribuyente*:

   - :ref:`Nueva Persona Física <alta-persona-fisica>`
   - :ref:`Nueva Persona Jurídica <alta-persona-juridica>`


.. _alta-persona-fisica:

Nueva Persona Física
----------------------

  Si el usuario desea crear una nueva *Persona Física*, deberá presionar el botón ``Nueva Persona Física``.

  A continuación, el sistema lo redirigirá a la siguiente pantalla. En esta parte, al usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Persona Física*.

  .. image:: _static/alta_personafisica.png
     :align: center


  .. ATTENTION::

      Se puede observar un botón verde con la leyenda ``Agregar`` en el campo *Nacionalidad*, así como en la sección domicilio en el campo *Localidad*, el cual es utilizado para
      agregar una nueva nacionalidad o localidad respectivamente si no se encuentran registradas en el sistema. Además;
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de contribuyentes.


.. _alta-persona-juridica:

Nueva Persona Jurídica
------------------------

  Si el usuario desea crear una nueva *Persona Jurídica*, deberá presionar el botón ``Nueva Persona Jurídica``.

  A continuación el sistema lo redirigirá a una pantalla, similar al registro de una nueva persona física.
  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Persona Jurídica*.
  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de contribuyentes.


.. _detalle-contribuyente:

Detalle de Contribuyente
------------------------

   Si el usuario desea ver el detalle de un *Contribuyente*, deberá seleccionar en la columna de **acciones** asociado al *Contribuyente* y
   presionar el ícono ``Detalle``

   Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

   .. image:: _static/detalle_contribuyente.png
      :align: center

   En esta parte el usuario podrá observar la información adicional del *Contribuyente*.
   Si desea volver al listado inicial, presionará el botón ``Regresar``.


.. _modificar-contribuyente:

Modificar Contribuyente
-----------------------

   Si el usuario desea modificar los datos de un *Contribuyente*, deberá seleccionar en la columna de **acciones** asociado al *Contribuyente* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image:: _static/mod_contribuyente.png
      :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados al *Contribuyente*.

   .. ATTENTION::

       Se puede observar  al igual que en la sección *Nueva Persona Física*, un botón verde con la leyenda ``Agregar`` en el campo *Localidad*, en el formulario del domicilio, el cual es utilizado para
       agregar una nueva localidad si no se encuentran registrada en el sistema. Además;
       El sistema recopilará los datos registrados del contribuyente y los mostrará para modificarlos, además, siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
       En este punto, las posibles causas de errores son:

           - Uno o más campos obligatorios vacíos.
           - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos del *Contribuyente* seleccionado.


.. _eliminar-contribuyente:

Eliminar Contribuyente
----------------------

   Si el usuario desea eliminar un *Contribuyente*, deberá seleccionar en la columna de **acciones** asociado al *Contribuyente* y presionar el ícono ``Eliminar``

   Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

   .. image:: _static/baja_contribuyente.png
      :align: center

   En esta parte el usuario deberá decidir si confirma la eliminación del *Contribuyente* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.
