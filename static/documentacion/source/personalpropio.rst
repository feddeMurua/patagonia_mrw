Personal Propio
===============
  Se presentará una pantalla que contendrá un listado con todos el *Personal Propio*
  que se encuentren registrados en el sistema hasta la fecha.

  .. image::_static/listado_pp.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Persona*.

  Estas funcionalidades son:

    - :ref:`Detalle Persona <detalle-persona>`
    - :ref:`Modificar Persona <modificar-persona>`
    - :ref:`Eliminar Persona <eliminar-persona>`

  Además, si el usuario desea Registrar una nueva *Persona*:

    - :ref:`Nueva Persona <nueva-persona>`


.. _nueva-persona:

Nueva Persona
-------------

  Si el usuario desea crear una nueva *Persona*, deberá presionar el botón ``Nueva Persona``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image::_static/alta_personafisica.png
     :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Persona*.

  .. ATTENTION::

      Se puede observar un botón verde con la leyenda ``Agregar`` en el campo *Nacionalidad*, así como en la sección domicilio en el campo *Localidad*, el cual es utilizado para
      agregar una nueva nacionalidad o localidad respectivamente si no se encuentran registradas en el sistema. Además;
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de personas.


.. _detalle-persona:

Detalle de Persona
------------------

   Si el usuario desea ver el detalle de una *Persona*, deberá seleccionar en la columna de **acciones** asociado a la *Persona* y presionar el ícono ``Detalle``

   Una vez realizado el paso anterior aparecerá la siguiente vista emergente:

   .. image::_static/detalle_personalpropio.png
      :align: center

   En esta parte el usuario podrá observar la información adicional de la *Persona*. Si desea volver al listado inicial, presionará el botón ``Regresar``.


.. _modificar-persona:

Modificar Persona
-----------------

   Si el usuario desea modificar los datos de una *Persona*, deberá seleccionar en la columna de **acciones** asociado a la *Persona* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image::_static/mod_personalpropio.png
      :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Persona*.

   .. ATTENTION::

       Se puede observar  al igual que en la sección *Nueva Persona*, un botón verde con la leyenda ``Agregar`` en el campo *Localidad*, en el formulario del domicilio, el cual es utilizado para
       agregar una nueva localidad si no se encuentran registrada en el sistema. Además;
       El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
       En este punto, las posibles causas de errores son:

           - Uno o más campos obligatorios vacíos.
           - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Persona* seleccionada.


.. _eliminar-persona:

Eliminar Persona
----------------

   Si el usuario desea eliminar una *Persona*, deberá seleccionar en la columna de **acciones** asociado a la *Persona* y presionar el ícono ``Eliminar``

   Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

   .. image::_static/baja_personalpropio.png
      :align: center

   En esta parte el usuario deberá decidir si confirma la eliminación de la *Persona* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.
