Menú de Usuarios
================
  Se presentará una pantalla que contendrá un listado con todos los *Usuarios*
  que se encuentren registrados en el sistema hasta la fecha.

  .. image:: _static/listado_usuario.png
    :align: center

  Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular cada *Usuario*.

  Estas funcionalidades son:

    - :ref:`Modificar Usuario <modificar-usuario>`
    - :ref:`Eliminar Usuario <eliminar-usuario>`

  Además, si el usuario desea Registrar un nuevo *Usuario*:

    - :ref:`Alta de Usuario <alta-Usuario>`


.. _alta-Usuario:

Alta de Usuario
---------------

  Si el administrativo desea crear un nuevo *Usuario*, deberá presionar el botón ``Alta de Usuario``.

  A continuación el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_usuario.png
    :align: center

  En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Usuario*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

          - Uno o más campos obligatorios vacíos.
          - Uno o más campos con un formato incorrecto.

      En caso de que el futuo usuario tenga permisos especiales, se deberá seleccionar la opción "Es staff".

  Una vez completado el formulario, se volverá  a la pantalla que contendrá el listado de cursos.


.. _modificar-Usuario:

Modificación de Usuario
-----------------------

  Si el usuario desea modificar los datos de un *Usuario*, deberá seleccionar en la columna de **acciones** asociado al *Usuario* y presionar el ícono ``Modificar``.

  Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

  .. image:: _static/alta_usuario.png
    :align: center

  En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados al *Usuario*.

  .. ATTENTION::
      El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
      En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.

   Una vez completado el formulario, el usuario deberá presionar el botón ``Aceptar`` y el sistema se encargará de actualizar los datos del *Usuario* seleccionado.


.. _eliminar-Usuario:

Eliminar Usuario
----------------

  Si el administrativo desea eliminar un *Usuario*, deberá seleccionar en la columna de **acciones** asociado al *Usuario* y presionar el ícono ``Eliminar``

  Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

  .. image:: _static/baja_usuario.png
    :align: center

  En esta parte el usuario deberá decidir si confirma la eliminación del *Usuario* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.
