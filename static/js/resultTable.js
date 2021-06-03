  $(document).ready(function() {
    var resultTable = $.ajax({
      url: "../static/result/resultChart.csv",
      dataType: 'text',
      success: function(data) {
        var allRow = data.split(/\r?\n|\r/);
        var table = '<table class="table table-hover" id="dontOverflow">';
        var header=['종목명','당일','다음주','다음달']
        var textLine = "";

        textLine += table;

        for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
          var collapse = allRow[singleRow].split(",");

          if (singleRow == 0) {
            textLine += '<thead class="text-centor" id="tableHead">';
            for (var count = 0; count < header.length;count++){
            textLine += '<th>' + header[count] + '</th>';
            }
            continue;
          }
          else if (singleRow == 1) {
            textLine += '<tbody class="text-left">';
          }

          textLine += '<tr>';

          for (var count = 0; count < collapse.length; count++) {
            if (singleRow == allRow.length - 1) continue;
            if (count==0){
              textLine += '<td>' + collapse[count] + '</td>';
            }
            else{
              if (count % 2 == 0) {
                if (collapse[count] == '상승') {
                  textLine += '<span class="text-danger">';
                }
                else if (collapse[count] == '하락') {
                  textLine += '<span class="text-primary">';
                }
                textLine += collapse[count]+'</span></td>';
              }
              else {
                textLine += '<td>' + collapse[count] + '의 확률로 ';
              }
            }
          }

          textLine += '</tr>';
          if (singleRow == 0) {
            textLine += '</thead>';
          }
        }
        textLine += '</tbody>';
        textLine += '</table>';

        $('#resultTable').append(textLine);
      }
    });
  })
