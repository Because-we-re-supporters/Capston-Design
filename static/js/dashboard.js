$(document).ready(function() {

  var chart = $.ajax({
    url: "static/data/dashboard/chart.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="table">';

      var KOSPItext = "";
      var KOSDAQtext = "";
      var KOSPI200text = "";
      var KOSPItable = "";
      var KOSDAQtable = "";
      var KOSPI200table = "";

      KOSPItext += table;
      KOSDAQtext += table;
      KOSPI200text += table;
      KOSPItable += table;
      KOSDAQtable += table;
      KOSPI200table += table;

      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");

        if (singleRow == allRow.length - 1) continue;
        if (singleRow == 0) {
          KOSPItext += '<tbody class="text-centor" style="border-top:none;">';
          KOSDAQtext += '<tbody class="text-centor" style="border-top:none;" >';
          KOSPI200text += '<tbody class="text-centor" style="border-top:none;">';
        }

        if (singleRow == 0) {
          KOSPItable += '<thead class="text-centor" id="tableHead">';
          KOSDAQtable += '<thead class="text-centor" id="tableHead">';
          KOSPI200table += '<thead class="text-centor" id="tableHead">';
        } else if (singleRow == 1) {
          KOSPItable += '<tbody class="text-centor">';
          KOSDAQtable += '<tbody class="text-centor">';
          KOSPI200table += '<tbody class="text-centor">';
        }




        for (var count = 0; count < collapse.length; count++) {
          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            if (count >= 5) {
              KOSPItable += '<td style="border-top:none;">' + "<h4>" + collapse[count] + "</h4>" + "</td>";
              KOSPI200table += '<td style="border-top:none;">' + "<h4>" + collapse[count] + "</h4>" + "</td>";
              KOSDAQtable += '<td style="border-top:none;">' + "<h4>" + collapse[count] + "</h4>" + "</td>";
            }
          } else {
            if (collapse[0] == "코스피200") {
              if (count == 4) {
                continue;
              } else if (count == 2) {
                if (collapse[4] == "상승") {
                  KOSPI200text += '<td class="text-danger" style="border-top:none;"><h4>' + '▲ ' + collapse[count] + '</h4></td>';
                } else if (collapse[4] == "하락") {
                  KOSPI200text += '<td class="text-primary" style="border-top:none;"><h4>' + '▼ ' + collapse[count] + '</h4></td>';
                } else {
                  KOSPI200text += '<td style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                }
              } else if (count == 1 || count == 3) {
                if (collapse[4] == "상승") {
                  KOSPI200text += '<td class="text-danger" style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                } else if (collapse[4] == "하락") {
                  KOSPI200text += '<td class="text-primary" style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                } else {
                  KOSPI200table += '<td><h4>' + collapse[count] + '</h4></td>';
                }
              } else if (count == 0) {
                KOSPI200text += '<td style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
              } else {
                if (parseInt(collapse[count]) > 0) {
                  KOSPI200table += '<td class="text-danger"><h4>' + collapse[count] + '억' + '</h4></td>';
                } else if (parseInt(collapse[count]) < 0) {
                  KOSPI200table += '<td class="text-primary"><h4>' + collapse[count] + '억' + '</h4></td>';
                } else {
                  KOSPI200table += '<td><h4>' + collapse[count] + '억' + '</h4></td>';
                }
              }
            } else if (collapse[0] == '코스피') {
              if (count == 4) {
                continue;
              } else if (count == 2) {
                if (collapse[4] == "상승") {
                  KOSPItext += '<td class="text-danger" style="border-top:none;"><h4>' + '▲ ' + collapse[count] + '</h4></td>';
                } else if (collapse[4] == "하락") {
                  KOSPItext += '<td class="text-primary" style="border-top:none;"><h4>' + '▼ ' + collapse[count] + '</h4></td>';
                } else {
                  KOSPItext += '<td style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                }
              } else if (count == 1 || count == 3) {
                if (collapse[4] == "상승") {
                  KOSPItext += '<td class="text-danger" style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                } else if (collapse[4] == "하락") {
                  KOSPItext += '<td class="text-primary" style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                } else {
                  KOSPItable += '<td><h4>' + collapse[count] + '</h4></td>';
                }
              } else if (count == 0) {
                KOSPItext += '<td style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
              } else {
                if (parseInt(collapse[count]) > 0) {
                  KOSPItable += '<td class="text-danger"><h4>' + collapse[count] + '억' + '</h4></td>';
                } else if (parseInt(collapse[count]) < 0) {
                  KOSPItable += '<td class="text-primary"><h4>' + collapse[count] + '억' + '</h4></td>';
                } else {
                  KOSPItable += '<td><h4>' + collapse[count] + '억' + '</h4></td>';
                }
              }
            } else if (collapse[0] == '코스닥') {
              if (count == 4) {
                continue;
              } else if (count == 2) {
                if (collapse[4] == "상승") {
                  KOSDAQtext += '<td class="text-danger" style="border-top:none;"><h4>' + '▲ ' + collapse[count] + '</h4></td>';
                } else if (collapse[4] == "하락") {
                  KOSDAQtext += '<td class="text-primary" style="border-top:none;"><h4>' + '▼ ' + collapse[count] + '</h4></td>';
                } else {
                  KOSDAQtext += '<td style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                }
              } else if (count == 1 || count == 3) {
                if (collapse[4] == "상승") {
                  KOSDAQtext += '<td class="text-danger" style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                } else if (collapse[4] == "하락") {
                  KOSDAQtext += '<td class="text-primary" style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
                } else {
                  KOSDAQtable += '<td><h4>' + collapse[count] + '</h4></td>';
                }
              } else if (count == 0) {
                KOSDAQtext += '<td style="border-top:none;"><h4>' + collapse[count] + '</h4></td>';
              } else {
                if (parseInt(collapse[count]) > 0) {
                  KOSDAQtable += '<td class="text-danger"><h4>' + collapse[count] + '억' + '</h4></td>';
                } else if (parseInt(collapse[count]) < 0) {
                  KOSDAQtable += '<td class="text-primary"><h4>' + collapse[count] + '억' + '</h4></td>';
                } else {
                  KOSDAQtable += '<td><h4>' + collapse[count] + '억' + '</h4></td>';
                }
              }
            }
          }
        }
        if (singleRow == 0) {
          KOSPItable += '</thead>';
          KOSPI200table += '</thead>';
          KOSDAQtable += '</thead>';
        } else {
          KOSPItable += '</tbody>';
          KOSPI200table += '</tbody>';
          KOSDAQtable += '</tbody>';
        }
      }
      KOSPItext += '</tbody>';
      KOSPItext += '</table>';
      KOSPI200text += '</tbody>';
      KOSPI200text += '</table>';
      KOSDAQtext += '</tbody>';
      KOSDAQtext += '</table>';

      KOSPItable += '</table>';
      KOSPI200table += '</table>';
      KOSDAQtable += '</table>';
      KOSPItext += KOSPItable;
      KOSPI200text += KOSPI200table;
      KOSDAQtext += KOSDAQtable;
      $('#KOSPItext').append(KOSPItext);
      $('#KOSPI200text').append(KOSPI200text);
      $('#KOSDAQtext').append(KOSDAQtext);

      //$('#KOSPItable').append(KOSPItable);
      //$('#KOSPI200table').append(KOSPI200table);
      //$('#KOSDAQtable').append(KOSDAQtable);
    }
  });
  var market_capitalization = $.ajax({
    url: "static/data/dashboard/market_capitalization.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      // table / thead / tr / th / td
      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 3) {
              if (collapse[count + 1] > 0) {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[count + 1] < 0) {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 4) {
              if (collapse[count] > 0) {
                textLine += '<td class="text-danger">' + '+' + collapse[count] + '%' + '</td>';
              } else if (collapse[count] < 0) {
                textLine += '<td class="text-primary">' + collapse[count] + '%' + '</td>';
              } else {
                textLine += '<td>' + '&nbsp' + '&nbsp' + collapse[count] + '%' + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#MarketCapitalizationTable').append(textLine);
      $('#MarketCapitalizationTable').append("<br>");
    }
  });
  var exchangeRate = $.ajax({
    url: "static/data/dashboard/exchangeRate.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      // table / thead / tr / th / td
      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {
          if (count == 3) continue;

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 1) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 2) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 3) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + '&nbsp' + '&nbsp' + collapse[count] + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#exchangeRateTable').append(textLine);
      $('#exchangeRateTable').append("<br>");
    }
  });
  var nationMarketRate = $.ajax({
    url: "static/data/dashboard/nationMarketRate.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      // table / thead / tr / th / td
      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {
          if (count == 3) continue;

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 1) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 2) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 3) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + '&nbsp' + '&nbsp' + collapse[count] + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#nationMarketRateTable').append(textLine);
      $('#nationMarketRateTable').append("<br>");
    }
  });
  var goldOil = $.ajax({
    url: "static/data/dashboard/goldOil.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      // table / thead / tr / th / td
      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {
          if (count == 3) continue;

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 1) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 2) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#goldOilTable').append(textLine);
      $('#goldOilTable').append("<br>");
    }
  });
  var interestRate = $.ajax({
    url: "static/data/dashboard/rate.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      // table / thead / tr / th / td
      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {


          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 2) {
              if (collapse[4] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[4] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 3) {
              if (collapse[4] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[4] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td> - </td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#interestRateTable').append(textLine);
      $('#interestRateTable').append("<br>");
    }
  });
  var energy = $.ajax({
    url: "static/data/dashboard/energy.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == allRow.length - 1) continue;
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {
          if (count == 4) continue;

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 3 || count == 6) {
              if (collapse[4] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[4] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 5) {
              if (collapse[4] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[4] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#energyTable').append(textLine);
      $('#energyTable').append("<br>");
    }
  });
  var nonMetal = $.ajax({
    url: "static/data/dashboard/nonMetal.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      // table / thead / tr / th / td
      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == allRow.length - 1) continue;
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {
          if (count == 3) continue;

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 4 || count == 2) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 5) {
              if (collapse[3] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[3] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#nonMetalTable').append(textLine);
      $('#nonMetalTable').append("<br>");
    }
  });
  var crops = $.ajax({
    url: "static/data/dashboard/crops.txt",
    dataType: 'text',
    success: function(data) {

      var allRow = data.split(/\r?\n|\r/);
      var table = '<table class="w-100 p-3 table table-hover" id="dontOverflow">';

      var textLine = "";
      textLine += table;
      for (var singleRow = 0; singleRow < allRow.length; singleRow++) {
        var collapse = allRow[singleRow].split(";");
        if (singleRow == allRow.length - 1) continue;
        if (singleRow == 0) {
          textLine += '<thead class="text-left" id="tableHead">';
        } else if (singleRow == 1) {
          textLine += '<tbody class="text-centor">';
        }
        textLine += '<tr>';
        for (var count = 0; count < collapse.length; count++) {
          if (count == 4) continue;

          if (singleRow == allRow.length - 1) continue;
          if (singleRow == 0) {
            textLine += '<th>' + collapse[count] + '</th>';
          } else {
            if (count == 3 || count == 6) {
              if (collapse[4] == "상승") {
                textLine += '<td class="text-danger">' + collapse[count] + '</td>';
              } else if (collapse[4] == "하락") {
                textLine += '<td class="text-primary">' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else if (count == 5) {
              if (collapse[4] == "상승") {
                textLine += '<td class="text-danger">' + '▲ ' + collapse[count] + '</td>';
              } else if (collapse[4] == "하락") {
                textLine += '<td class="text-primary">' + '▼ ' + collapse[count] + '</td>';
              } else {
                textLine += '<td>' + collapse[count] + '</td>';
              }
            } else {
              textLine += '<td>' + collapse[count] + '</td>';
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

      $('#cropsTable').append(textLine);
      $('#cropsTable').append("<br>");
    }
  });
})
