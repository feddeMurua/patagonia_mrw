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


.. _nueva-inscripcion:

Nueva Inscripción
-----------------

  Si el usuario desea crear una nueva *Inscripción*, deberá presionar el botón ``Nueva Inscripción``.

  A continuación, el sistema lo redirigirá a la siguiente pantalla. En esta parte, al usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Inscripción*.

  .. image:: _static/alta_inscripcion.png
     :align: center


  .. ATTENTION::

      Se puede observar un botón verde con la leyenda ``Agregar`` en el campo *Persona*, el cual es utilizado para
      agregar una nueva persona respectivamente si no se encuentra registrada en el sistema. Además;
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de inscripciones.


.. _eliminar-inscripcion:

Eliminar Inscripción
--------------------

  Si el usuario desea eliminar una *Inscripción*, deberá seleccionar en la columna de **acciones** asociado a la *Inscripción* y presionar el ícono ``Eliminar``

  Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

  .. image:: _static/baja_inscripcion.png
     :align: center

  En esta parte el usuario deberá decidir si confirma la eliminación de la *Inscripción* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.


.. _modificar-inscripcion:

Modificar Inscripción
---------------------

   Si el usuario desea modificar los datos de una *Inscripción*, deberá seleccionar en la columna de **acciones** asociado a la *Inscripción* y presionar el ícono ``Modificar``.

   Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

   .. image:: _static/mod_inscripcion.png
      :align: center

   En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Inscripción*.

   .. ATTENTION::

       El sistema recopilará los datos registrados de la Inscripción y los mostrará para modificarlos, además, siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
       En este punto, las posibles causas de errores son:

           - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos de la *Inscripción* seleccionada.


.. _imprimir-inscripcion:

Imprimir Inscripción
--------------------

  Si el usuario desea imprimir una *Inscripción*, deberá seleccionar en la columna de **acciones** asociado a la *Inscripción* y presionar el ícono ``Imprimir Comprobante``

  A continuación, el sistema presentará en una nueva pestaña un archivo en formato .PDF para imprimir el comprobante de inscripción.
