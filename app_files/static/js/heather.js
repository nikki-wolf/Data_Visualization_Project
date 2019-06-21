var countryUnpack
var priceUnpack
var ratingUnpack
var varietyUnpack
var uniqueID;

function myParallel() {
  var url = "/api_rating_extended";
  d3.json(url).then(function(wineData) {
    console.log(wineData)
    
      function unpack(rows, key) {
        return rows.map(function(row) { 
           return row[key]; 
         });
        }
        countryUnpack = unpack(wineData, 'country');
        console.log(countryUnpack, 'Unpacked Countries')

        priceUnpack = unpack(wineData, 'price')
        console.log(priceUnpack, 'unpacked prices')

        ratingUnpack = unpack(wineData, 'rating')
        console.log(ratingUnpack, 'unpacked ratings')

        varietyUnpack = unpack(wineData, 'variety')
        console.log(varietyUnpack, 'unpacked variety')


           uniqueID = countryUnpack.filter((v, i, a) => a.indexOf(v) === i);
         console.log(uniqueID);

      
     
      var data = [{
        type: 'parcoords',
        visible: true,
        line: {
          showscale: true,
          reversescale: true,
          colorscale: 'Jet',
          cmin: 1,
          cmax: 3000,
          color:  uniqueID
        },
       
        dimensions: [{
          range: [0,43],
          tickvals: Array.apply(0,new Array(43)).map(function(_,i){ return i+1 }),
          ticktext: uniqueID,
          label: 'Countries',
          values: uniqueID
        }, {
          constraintrange: [2000,2500],
          range: [Math.min(...priceUnpack),
          Math.max(...priceUnpack)],
          label: 'Price',
          values: priceUnpack,
          multiselect:true
        
        }, {
          constraintrange: [86,90],
          multiselect: true,
          label: 'Rating',
          range: [80,
          Math.max(...ratingUnpack)],
          values: ratingUnpack
        }, {
          label: 'Variety',
          range: [0,6],
          tickvals: Array.apply(0,new Array(6)).map(function(_,i){ return i+1 }),
          ticktext: varietyUnpack,
          values: varietyUnpack
    
        }
        ]
      }];
      var layout = {
        width: 710,
        height: 620
      };
  
    
      Plotly.plot('heatherDiv', data, layout);
    });
  }
myParallel()