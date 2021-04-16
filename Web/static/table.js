$(document).ready(function() {
    // create a data table from existing html table
    table = $('#table').DataTable();

    // set event handler for row click
    $('#table tbody').on('click', 'tr', function () {
	var rowthis = this; 	                  
        var row = table.row( this ).data();       
	setInterval(function(){
	    table.ajax.reload(null,false);},5000);
    } );
} );
