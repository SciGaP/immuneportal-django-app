

function CSVToArray(strData, strDelimiter) {
    // Check to see if the delimiter is defined. If not,
    // then default to comma.
    strDelimiter = (strDelimiter || "\t");
    // Create a regular expression to parse the CSV values.
    var objPattern = new RegExp((
    // Delimiters.
    "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +
    // Quoted fields.
    "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +
    // Standard fields.
    "([^\"\\" + strDelimiter + "\\r\\n]*))"), "gi");
    // Create an array to hold our data. Give the array
    // a default empty first row.
    var arrData = [[]];
    // Create an array to hold our individual pattern
    // matching groups.
    var arrMatches = null;
    // Keep looping over the regular expression matches
    // until we can no longer find a match.
    while (arrMatches = objPattern.exec(strData)) {
        // Get the delimiter that was found.
        var strMatchedDelimiter = arrMatches[1];
        // Check to see if the given delimiter has a length
        // (is not the start of string) and if it matches
        // field delimiter. If id does not, then we know
        // that this delimiter is a row delimiter.
        if (strMatchedDelimiter.length && (strMatchedDelimiter != strDelimiter)) {
            // Since we have reached a new row of data,
            // add an empty row to our data array.
            arrData.push([]);
        }
        // Now that we have our delimiter out of the way,
        // let's check to see which kind of value we
        // captured (quoted or unquoted).
        if (arrMatches[2]) {
            // We found a quoted value. When we capture
            // this value, unescape any double quotes.
            var strMatchedValue = arrMatches[2].replace(
            new RegExp("\"\"", "g"), "\"");
        } else {
            // We found a non-quoted value.
            var strMatchedValue = arrMatches[3];
        }
        // Now that we have our value string, let's add
        // it to the data array.
        arrData[arrData.length - 1].push(strMatchedValue);
    }
    // Return the parsed data.
    return (arrData);
}




function CSV2JSON(csv) {
    var array = CSVToArray(csv);
    var objArray = [];
    for (var i = 1; i < array.length; i++) {
        objArray[i - 1] = {};
        for (var k = 0; k < array[0].length && k < array[i].length; k++) {
            var key = array[0][k];
            objArray[i - 1][key] = array[i][k]
        }
    }
    return (array);
}

function transpose(a) {

  // Calculate the width and height of the Array
  var w = a.length || 0;
  var h = a[0] instanceof Array ? a[0].length : 0;

  // In case it is a zero matrix, no transpose routine needed.
  if(h === 0 || w === 0) { return []; }

  /**
   * @var {Number} i Counter
   * @var {Number} j Counter
   * @var {Array} t Transposed data is stored in this array.
   */
  var i, j, t = [];

  // Loop through every item in the outer array (height)
  for(i=0; i<h; i++) {

    // Insert a new row (array)
    t[i] = [];

    // Loop through every item per item in outer array (width)
    for(j=0; j<w; j++) {

      // Save transposed data.
      t[i][j] = a[j][i];
    }
  }

  return t;
}


function numInstance(arr) {
  var a = [],
    b = [],
    prev;

  arr.sort();
  for (var i = 0; i < arr.length; i++) {
    if (arr[i] !== prev) {
      a.push(arr[i]);
      b.push(1);
    } else {
      b[b.length - 1]++;
    }
    prev = arr[i];
  }

  return [a, b];
}


$.ajax({
	    url: 'http://localhost:8000/static/files/test_Aligned.sortedByCoord.out_intron_candidates_weak_bind_peptide_predict_result.txt',
	    method: 'GET',
	    //datatype: 'json',
	    
	    
       	    //console.log(data_file);
            //console.log(data_file);
	    success: function (data) {
	    	console.log('rawout',data);
	    	var output=CSV2JSON(data);
	    	console.log('postfunc',output);
	   
function makeTrace(i) {
    //console.log('exists',numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('hla')]));
    if (i==output[0].indexOf('hla')){
    return {
    	type: 'pie',
    	title: 'HLA Type Distribution',
        labels:numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('hla')])[0],
        values:numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('hla')])[1],
        
        visible: i === 0,
       
      

    }
   }
  else if(i==output[0].indexOf('mut_pep')){
    return {
        type: 'bar',
        title: 'Mut Pep Distribution',
        
        x:numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('mut_pep')])[0],
        y:numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('mut_pep')])[1],
        
        visible: i === 0,
      
      

    }
  }
  else{
    return {
        type: 'bar',
        title: 'Wt Pep Distribution',
        
        x:numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('wt_pep')])[0],
        y:numInstance(transpose(output.slice(1,output.length))[output[0].indexOf('wt_pep')])[1],
        
        visible: i === 0,
        
      

    }
  }
}
console.log('json',output);         
            
var myPlot= document.getElementById('myDiv');

//Plotly.newPlot('myDiv', data, layout);


Plotly.newPlot('myDiv', [output[0].indexOf('hla'), output[0].indexOf('mut_pep'), output[0].indexOf('wt_pep')].map(makeTrace), {
    updatemenus: [{
        
        
        yanchor: 'top',
        buttons: [{
            method: 'restyle',
            args: ['visible', [true, false, false]],
            label: 'HLA type'
        }, {
            method: 'restyle',
            args: ['visible', [false, true, false]],
            label: 'Mut Pep'
        }, {
            method: 'restyle',
            args: ['visible', [false, false, true]],
            label: 'totalTable'
        }]
    }],
});
/*

	    $.fn.dataTable.ext.errMode = 'throw';
	    $('#resultTable').DataTable( {
		    "processing": true,
		"scrollX": true,
		"data":output,
	    } );
	    var table = $('#resultTable').DataTable();*/
/*
var data = [{
  type: 'table',
  header: {
    values: output[0],
    align: "center",
    line: {width: 1, color: 'black'},
    fill: {color: "grey"},
    font: {family: "Arial", size: 12, color: "white"}
  },
  cells: {
    values: transpose(output.slice(1,output.length)),
    align: "center",
    line: {color: "black", width: 1},
    font: {family: "Arial", size: 11, color: ["black"]}
  }
}]

Plotly.newPlot('myPltTable', data);

//CLICK EVENTS FOR PLOT TO UPDATE TABLE

myPlot.on('plotly_click', function(data){
    console.log(data);
    
    var newData=[];
    var curveNumber=data.points[0].curveNumber;
    for (i=1;i<output.length;i++){
    	//probability curve
    	if(curveNumber==0){
    		if(output[i].includes(data.points[0].y)){
    			newData.push(output[i]);
    		}
    	}
    	else if(curveNumber==1){
    		if(output[i].includes(data.points[0].x)){
    			newData.push(output[i]);
    		}
    	}
    	else if(curveNumber==2){
    		if(output[i].includes(data.points[0].x)){
    			newData.push(output[i]);
    		}
    	}
    }
    
    var data = [{
	  type: 'table',
	  header: {
	    values: output[0],
	    align: "center",
	    line: {width: 1, color: 'black'},
	    fill: {color: "grey"},
	    font: {family: "Arial", size: 12, color: "white"}
	  },
	  cells: {
	    values: transpose(newData.slice(0,newData.length)),
	    align: "center",
	    line: {color: "black", width: 1},
	    font: {family: "Arial", size: 11, color: ["black"]}
	  }
	}]
    //document.getElementById("myPltTable").setAttribute('data',data);
    //Plotly.redraw('myPltTable');
    Plotly.newPlot('myPltTable', data);

    
    /*var pts = '';
    for(var i=0; i < data.points.length; i++){
        pts = 'x = '+data.points[i].x +'\ny = '+
            data.points[i].y.toPrecision(4) + '\n\n';
    }
    alert('Closest point clicked:\n\n'+pts);
});*/





}
	    });




