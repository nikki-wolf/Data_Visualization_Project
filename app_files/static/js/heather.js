// d3.json(url).then(function(wineData) {
//   console.log(wineData)
//   wineData.forEach(function(data) {
//     console.log(data);
//     console.log(data.Country)
//     console.log(JSON.parse(data.Price.replace(/\bnan\b/g, "null"))[0])
//     console.log(JSON.parse(data.Rating.replace(/\bnan\b/g, "null"))[0])
//     // console.log(JSON.parse(data.Variety.replace(/\bnan\b/g, "null"))[0])
//     console.log(eval('('+data.Variety+')')[0])
//   });
    console.log('helloooooooooooooo')
  
// });

var countries
var price
var rating
var varieties;

function myParallel() {
  var url = "/api_rating";
  d3.json(url).then(function(wineData) {
    console.log(wineData)
    
      function unpack(rows, key) {
        return rows.map(function(row) { 
           return row[key]; 
         });
        }
        var countryUnpack = unpack(wineData, 'Country');
        console.log(countryUnpack, 'Unpacked Countries')

        var priceUnpack = unpack(wineData, 'Price')
        console.log(priceUnpack)

        var ratingUnpack = unpack(wineData, 'Rating')
        console.log(ratingUnpack)


        var varietyUnpack = unpack(wineData, 'Variety')
        console.log(varietyUnpack)

        wineData.forEach(function(data){
          // countries = data.Country
          price = JSON.parse(data.Price.replace(/\bnan\b/g, "null"))
          console.log(price)
          rating = JSON.parse(data.Rating.replace(/\bnan\b/g, "null"))
          console.log(rating)
          varieties = eval('('+data.Variety+')')})
          console.log(varieties)
          ;
  
     
      // var cleanprice = price.map(function(d){
      //   if (d==null){
      //     return 0
      //   }
      //   return d;
      // });
      // console.log(cleanprice)

      // var rating = unpack(wineData, 'Rating')
      // console.log(rating, 'unpacked rating')
      // var rating = JSON.parse(wineData.Rating.replace(/\bnan\b/g, "null"), 'Rating');
      // var rating = JSON.parse(ratingUnpack.Rating.replace(/\bnan\b/g, "null"));
      // var parserating = rating.map(function(d){
      //   if (d==null){
      //     return 0
      //   }
      //   return d;
      // });
      // console.log(parserating)

      // var varietyUnpack = unpack(wineData, 'Variety');
      // var variety = eval('('+varietyUnpack.Variety+')');
      // console.log(variety)
  

      

      var data = [{
        type: 'parcoords',
        pad: [80,80,80,80],
        line: {
          showscale: true,
          // color: ,
          cmin: 1,
          cmax: 100,
          colorscale: 'Bluered,'
        },
      
        dimensions: [{
          range: [0,43],
          tickvals: countryUnpack,
          ticktext: countryUnpack,
          label: 'Countries',
          values: countryUnpack
        
        }, {
          constraintrange: [10,20],
          range: [Math.min(...price),
          Math.max(...price)],
          label: 'Price',
          values: priceUnpack
            
  
        }, {
          constraintrange: [0,3],
          label: 'Rating',
          range: [Math.min(...rating),
          Math.max(...rating)],
          values: ratingUnpack
        }, {
          constraintrange: [0,3],
          label: 'Variety',
          range: [0,42],
          tickvals: varietyUnpack,
          ticktext: varietyUnpack,
          values: varietyUnpack
        }
      ]
      }];
      
      var layout = {
        width: 700,
        height: 300
      };
      
      Plotly.plot('graphDiv', data, layout);
    });
  }
myParallel()

// var url = "/api_rating";
// d3.json(url).then(function(wineData) {
//   console.log(wineData)
  // wineData.forEach(function(data){
    // countries = data.Country
    // price = JSON.parse(data.Price.replace(/\bnan\b/g, "null"))
    // rating = JSON.parse(data.Rating.replace(/\bnan\b/g, "null"))
    // varieties = eval('('+data.Variety+')')})
  //   ;

  // function unpack(rows, key) {
  //   return rows.map(function(row) { 
  //      return row[key]; 
  //     });
  //   }
    // countries = data.Country
    // price = JSON.parse(data.Price.replace(/\bnan\b/g, "null"))
    // rating = JSON.parse(data.Rating.replace(/\bnan\b/g, "null"))
    // varieties = eval('('+data.Variety+')')})


  // var data = [{
  //     type: 'parcoords',
  //     pad: [80,80,80,80],
  //     line: {
  //       color: (wineData.countries, 'Countries'),
  //       colorscale: [[0, 'purple'], [0.5,'red'] , [1, 'pink']]
  //     },
    
  //     dimensions: [{
  //       range: [0,20],
  //       label: 'Countries',
  //       values: unpack(wineData.map(d => d.Country), 'Countries')
      
  //     }, {
  //       constraintrange: [5, 6],
  //       range: [0,20],
  //       label: 'Price',
  //       values: wineData.map(d => d.Price)
          
  //       // values: JSON.parse(data.Price.replace(/\bnan\b/g, "null"))
  //       // values: unpack(d3.extent(wineData.map(d => d.Price)))
  //       // d3.max(populationData.map(d=>d.poverty))
  //     }, {
  //       label: 'Rating',
  //       range: [0, d3.max(wineData.map(d => d.Rating))],
  //       values: unpack(wineData.map(d => d.Rating), "Rating")
  //     }, {
  //       label: 'Variety',
  //       range: [1, 7],
  //       values: unpack(wineData.map(d => d.Variety), 'Variety')
  //     }]
  //   }];
    
  //   var layout = {
  //     width: 800
  //   };
    
  //   Plotly.plot('graphDiv', data, layout);


  // });