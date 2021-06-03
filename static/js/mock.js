$(document).ready(function() {
  var kospiChart = $.ajax({
    url: "../static/result/kospi_table.csv",
    dataType: 'text',
    success: function(data) {
      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="table" id="dontOverflow">';
      var textLine = "";

      textLine += table;

      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(",");
        if (singleRow == 0) {
          textLine += '<thead class="text-centor" id="tableHead">';
        }
        else if (singleRow == 1) {
          textLine += '<tbody class="text-left">';
        }

        textLine += '<tr>';

        for (var count = 0; count < collapse.length; count++) {
          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0){
            textLine += '<th>' + collapse[count] + '</th>';
          }
          else{
            textLine += '<td>' + collapse[count] + '</td>';
          }
        }

        textLine += '</tr>';
        if (singleRow == 0) {
          textLine += '</thead>';
        }
      }
      textLine += '</tbody>';
      textLine += '</table>';

      $('#kospiChart').append(textLine);
    }
  });
  var kosdaqChart = $.ajax({
      url: "../static/result/kosdaq_table.csv",
      dataType: 'text',
      success: function(data) {
        var allRow = data.split(/\r?\n|\r/);
        var table = '<table class="table" id="dontOverflow">';
        var textLine = "";

        textLine += table;

        for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
          var collapse = allRow[singleRow].split(",");
          if (singleRow == 0) {
            textLine += '<thead class="text-centor" id="tableHead">';
          }
          else if (singleRow == 1) {
            textLine += '<tbody class="text-left">';
          }

          textLine += '<tr>';

          for (var count = 0; count < collapse.length; count++) {
            if (singleRow == allRow.length - 1) continue;
            if (singleRow == 0){
              textLine += '<th>' + collapse[count] + '</th>';
            }
            else{
              textLine += '<td>' + collapse[count] + '</td>';
            }
          }

          textLine += '</tr>';
          if (singleRow == 0) {
            textLine += '</thead>';
          }
        }
        textLine += '</tbody>';
        textLine += '</table>';

        $('#kosdaqChart').append(textLine);
      }
    });
})
