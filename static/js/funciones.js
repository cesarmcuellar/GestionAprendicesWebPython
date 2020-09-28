//función de inicio Jquery
var primeraFila; //variable global
var contactos = [];
$(function(){   
    //listarContactos();   
    //almacenando la primera fila de la tabla
    primeraFila = $("#fila"); 

    
    /**
     * Acción del evento click del botón
     * llamado btnConsultar
     */
    $("#btnConsultar").click(function(){       
        if ($("#txtIdentificacion").val()!==""){
            $("#idContacto").val(""); //campo oculto           
            consultarContacto();
        }else{
            alert("Debe ingresar la identificación del Contacto");
            $("#txtIdentificacion").focus();
        }
    });  

    /*El botón agregar se coloca como tipo submit para hacer las
    validaciones de los controles con html5*/
  
    $("#btnAgregar").click(function(){     
        agregarContacto();  
    });     
    
    $("#btnActualizar").click(function(){         
        if ($("#idContacto").val()===""){
            alert("Debe primero Consultar un Contacto");   
            $("#txtIdentificacion").focus();
        }else{
            actualizarContacto();
        } 
    }); 

    /*Primero se abre la ventana modal y a partir de ella se llama
    el método que hace el ajax*/
    $("#btnEliminar").click(function(){        
        if ($("#idContacto").val()===""){
           alert("Debe primero hacer una consulta de un Contacto");
           $("#txtIdentificacion").focus();
        }else{
            $("#modalEliminar").modal();
        }
    });    
    //Botón si del Modal de Eliminar Aprendiz
    $("#btnSiModal").click(function(){
        eliminarContacto();
    });  
    
    $("#btnListar").click(function(){
        listarContactos();
    });  
    
    $("#txtIdentificacion").change(function(){
        //existeContacto();
    });
    
 });

/**
 * Método que mediante ajax hace una petición al servidor
 * para agregar un contacto a la base de datos
 * @returns true o false
 */
function agregarContacto(){   
    $("#mensaje").html(""); 
    var formData = new FormData($("#frmContacto")[0]);  
    $.ajax({
        url: '/agregarContacto',    
        data: formData,
        dataType:'json',
        type: 'post',       
        cache: false,
        contentType: false,
        processData: false,
        success: function (resultado) {
            console.log(resultado); 
            if(resultado.estado){
                limpiar();
            }           
            $("#mensaje").html(resultado.mensaje);   
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}
/**
 * Método que consulta un aprendiz dada la identificación
 * realiza un llamado mediante Ajax.
 * @returns Objeto Aprendiz en formato Json
 */
function consultarContacto(){
    $("#mensaje").html(""); //div para mostrar mensajes    
    var identificacion = $("#txtIdentificacion").val();
    limpiar(); //función que limpia las cajas de texto
    $("#txtIdentificacion").val(identificacion);  
    var parametros = {
        identificacion:$("#txtIdentificacion").val()
    }  
    $.ajax({       
        url: '/consultarContacto',      
        data: parametros,
        type: 'post', 
        dataType: 'json',  
        cache: false,
        success: function (resultado) {
            console.log(resultado);
            var contacto = resultado.datos;
            if (resultado.estado){                
                $("#idContacto").val(contacto[0]);
                $("#txtIdentificacion").val(contacto[1]);
                $("#txtNombres").val(contacto[2]);
                $("#txtApellidos").val(contacto[3]);
                $("#txtCorreo").val(contacto[4]);
                //Conversión de la fecha                
                f = new Date(contacto[5])
                year= f.getUTCFullYear();
                mes = f.getUTCMonth();
                mes = mes < 9 ? "0" + (mes+1) : mes+1;                
                dia = f.getUTCDate();
                fecha = year + "-" + mes + "-" + dia;                          
                $("#txtFechaNacimiento").val(fecha);
            }else{
                $("#mensaje").html(resultado.mensaje);
            }
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });    
}

/**
 * Método que actualiza un aprendiz de acuerdo al
 * id del Aprendiz. Se envía los datos mediante Ajax.
 * @returns true o false
 */
function actualizarContacto(){
    $.ajax({       
        url: '/actualizarContacto',      
        data:$("#frmContacto").serialize(),
        dataType:'json',
        type: 'post',                     
        cache: false,
        success: function (resultado) {
            console.log(resultado);
            if (resultado.estado){  
                limpiar(); //limpia las cajas de texto           
            } 
            $("#mensaje").html(resultado.mensaje);
        },
        error: function(ex){
          console.log(ex.responseText);
        }  
    });
}

/**
 * Método que limpia las cajas de texto
 * @returns
 */

function eliminarContacto(){
    var parametros={
        idContacto:$("#idContacto").val()           
    }; 
    $.ajax({       
        url: '/eliminarContacto',      
        data:parametros,
        type: 'post', 
        dataType: 'json',  
        cache: false,
        success: function (resultado) {
            console.log(resultado);
            if (resultado.estado){               
                limpiar();
                listarContactos(); 
            }
            $("#mensaje").html(resultado.mensaje);
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

/**
 * Obtener listado de aprendices mediante
 * ajax.
 * @returns lista de aprendices objeto Json
 */
function listarContactos(){     
    $("#tblContactos").show();
    $("#mensaje").html("");
    //eliminar los datos de la tabla    
    $(".otraFila").remove();
    //agregar la primera fila vacía
    $("#tblContactos tbody").append(primeraFila);   
    $.ajax({       
        url: '/listarContactos',     
        type: 'post', 
        dataType: 'json',  
        cache: false,
        success: function (resultado) {
            console.log(resultado); 
            contactos = resultado.datos;
            $.each(contactos, function (i, contacto) {
                $("#aIdentifica").html(contactos[i][0]);
                $("#aNombres").html(contactos[i][1]);
                $("#aApellidos").html(contactos[i][2]);
                $("#aCorreo").html(contactos[i][3]);
                $("#aGenero").html(contactos[i][4]);    
                var f = new Date(contacto[5])
                var year= f.getUTCFullYear();
                var mes = f.getUTCMonth();
                mes = mes < 9 ? "0" + (mes+1) : mes+1;                
                var dia = f.getUTCDate();
                var fecha = year + "-" + mes + "-" + dia;    
                $("#aFechaNacimiento").html(fecha);   
                $("#tblContactos tbody").append($("#fila").clone(true).attr("class","otraFila"));
            });
            $("#tblContactos tbody tr").first().remove(); 
           
        },
        error: function(ex){
          console.log(ex.responseText);
        }
    });
}

/**
 * Método que limpia las cajas de texto
 * @returns {No retorna nada}
 */
function limpiar(){ 
    $("#txtIdentificacion").val("");
    $("#txtNombres").val("");
    $("#txtApellidos").val("");
    $("#txtCorreo").val("");    
    $("#txtFechaNacimiento").val(""); 
}



