function unpack(rows, key) {
    console.log(rows)
      return rows.map(function(row) {
          console.log(row[key])
        return row[key];
      });
    }
          d3.csv("../static/data/KOSPI.csv", function(err, rows) {
            var trace1 = {
              type: "scatter",
              mode: "lines",
              name: 'actual',
              x: unpack(rows, 'date'),
              y: unpack(rows, 'actual'),
              line: {
                color: '#17BECF'
              }
            }
            var trace2 = {
              type: "scatter",
              mode: "lines",
              name: 'prediction',
              x: unpack(rows, 'date'),
              y: unpack(rows, 'prediction'),
              line: {
                color: '#7F7F7F'
              }
            }
            var data = [trace1, trace2];
            var layout = {
              title: 'test',
            };
            Plotly.newPlot('myDiv', data, layout);
          });


/*function makeplot() {
  var x = [], y1 = [], y2 = [];
  Plotly.d3.csv("../static/data/KOSPI.csv", function(data){
    console.log(data);
    for (var i=0; i<data.length; i++){
      row = data[i];
      console.log(row[0],row[1],row[2]);
      x.push( row['N'] );
      y1.push( row['prediction'] );
      y2.push( row['actual'] );
    }
    console.log(x,y1,y2);
  });}

function processData(allRows) {
  var x = [], y1 = [], y2 = [];
  for (var i=0; i<allRows.length; i++) {
    row = allRows[i];
    x.push( row['N'] );
    y1.push( row['prediction'] );
    y2.push( row['actual'] );
  }
  console.log( 'X',x, 'pred',y1, 'act',y2);
  makePlotly( x, y1, y2 );
}

function makePlotly( x, y1, y2 ){
    //var plotDiv = document.getElementById("plot");
  var trace1 = {
    type: "scatter",
    mode: "lines",
    name: 'prediction',
    x: x,
    y: y1,
    line: {color: '#7F7F7F'}
  }
  var trace2 = {
    type: "scatter",
    mode: "lines",
    name: 'actual',
    x: x,
    y: y2,
    line: {color: '#17BECF'}
  }
  var data = [trace1,trace2];

  Plotly.newPlot('myDiv', data,
    {title: 'Plotting CSV data'});
};

makeplot();
*/



