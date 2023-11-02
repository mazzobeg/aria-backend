// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    "autoWidth": true,
    // "columns": [
    //   {"width": "50%"},
    //   {"width": "50%"},
    //   null    
    // ],
    "fixedColumns": {
      right:1
    }
  })
});
