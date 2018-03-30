Inscripciones
=============
  Se presentará una pantalla que contendrá un listado con todos las *Inscripciones* de un curso particular
  que se encuentren registrados en el sistema hasta la fecha.

  .. image:: _static/inscripcion_curso.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Inscripción*.

  Estas funcionalidades son:

   - :ref:`Eliminar Inscripción <eliminar-inscripcion>`
   - :ref:`Modificar Inscripción <modificar-inscripcion>`
   - :ref:`Imprimir Inscripción <imprimir-inscripcion>`

   Además, si el usuario desea Registrar una nueva *Inscripción*:

   - :ref:`Nueva Inscripción <nueva-inscripcion>`


.. _eliminar-inscripcion:

Eliminar Inscripción
----------------------

  Si el usuario desea eliminar una *Inscripción*, deberá seleccionar en la columna de **acciones** asociado a la *Inscripción* y presionar el ícono ``Eliminar``

  Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

  .. image:: _static/baja_inscripcion.png
     :align: center

  En esta parte el usuario deberá decidir si confirma la eliminación del *inscripcion* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


Modificar inscripcion
-----------------------

   Si el usuario desea modificar los datos de un *inscripcion*, deberá seleccionar en la columna de **acciones** asociado al *inscripcion* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image:: _static/mod_inscripcion.png
      :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados al *inscripcion*.

   .. ATTENTION::

       Se puede observar  al igual que en la sección *Nueva Persona Física*, un botón verde con la leyenda ``Agregar`` en el campo *Localidad*, en el formulario del domicilio, el cual es utilizado para
       agregar una nueva localidad si no se encuentran registrada en el sistema. Además;
       El sistema recopilará los datos registrados del inscripcion y los mostrará para modificarlos, además, siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
       En este punto, las posibles causas de errores son:

           - Uno o más campos obligatorios vacíos.
           - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos del *inscripcion* seleccionado.


.. _nueva-inscripcion:

Nueva Inscripción
-----------------

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

 Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de inscripcions.
