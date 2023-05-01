# Auto-Alembic

Este modulo ayuda a la ejecucion automatica de alembic, se encarga de comprobar si hay cambios por realizar y de haberlos, ejecutarlos de forma correcta.

Te ahorrará tener que ejecutar alembic de forma manual.

## ¿Cómo usar?

    import auto_alembic_module

    print(alembic_auto_upgrade())

    #salida: head upgraded
    
## Mensajes de error

<strong>"head upgraded"</strong> se aplicaron todos los cambios correctamente

<strong>"not changes detected"</strong> la base de datos esta actualizada y hay cambios pendientes

<strong>"errors in generate revision"</strong> ocurrio algun error mientras se generaba la revision

<strong>"upgrade errors"</strong> ocurrio algun error mientras se aplicaban los cambios

## Archivo de "log" o registro

Por defecto el "log" o "registro" está activado y almacena todos los cambios en un archivo "auto_alembic.log"
