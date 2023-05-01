# Auto-Alembic

Este modulo ayuda a la ejecucion automatica de alembic, se encarga de comprobar si hay cambios por realizar y de haberlos, ejecutarlos de forma correcta.

Te ahorrará tener que ejecutar alembic de forma manual.

## ¿Cómo usar?

    from auto_alembic_module import alembic_auto_upgrade

    print(alembic_auto_upgrade())

    #salida: head upgraded
    
## Mensajes de error

<strong>"head upgraded"</strong> se aplicaron todos los cambios correctamente

<strong>"not changes detected"</strong> la base de datos esta actualizada y hay cambios pendientes

<strong>"errors in generate revision"</strong> ocurrio algun error mientras se generaba la revision

<strong>"upgrade errors"</strong> ocurrio algun error mientras se aplicaban los cambios

## Funcion alembic_auto_upgrade
    
"alembic_auto_upgrade" recibe como parametro opcional una cadena de texto, dicha cadena sirve para comentar la revision generada.

        def alembic_auto_upgrade(message:str = ""):

Si a "alembic_auto_upgrade" no se le entrega ningun parametro, está generará un comentario de forma automatica a travez de la funcion "alembic_generate_commit_message".
    
## Archivo de "log" o registro

Por defecto el "log" o "registro" está activado y almacena todos los cambios en un archivo "auto_alembic.log"
