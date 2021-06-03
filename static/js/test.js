var x=[], y1=[], y2=[];
d3.csv("../static/data/KOSPI.csv", function(rows) {
    x.push(parseInt(rows.date));
    y1.push(parseFloat(rows.actual));
    y2.push(parseFloat(rows.prediction));

    /*for(var i=0; i<rows.length;i++){
        row=rows[i];
        console.log(row.date,row.actual,row.prediction);
        x.push(row.date);
        y1.push(row.actual);
        y2.push(row.prediction);
    }*/
});

var trace1 = {
    type: "scatter",
    mode: "lines",
    name: 'actual',
    x: x,
    y1: y1,
    line: {
      color: '#17BECF'
    }
  }
  var trace2 = {
    type: "scatter",
    mode: "lines",
    name: 'prediction',
    x: x,
    y2: y2,
    line: {
      color: '#7F7F7F'
    }
  }
  var data = [trace1, trace2];
  console.log(trace1,trace2);
  Plotly.newPlot('myDiv', data, layout);

/*
function unpack(rows, key) {
  console.log(rows)
  return rows.map(function(row) {
    console.log(rows[key])
    return row[key];
  });
}

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
  */