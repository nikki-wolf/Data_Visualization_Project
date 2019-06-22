// global variables
var countryUnpack
var priceUnpack
var ratingUnpack
var varietyUnpack
var uniqueCountry
var uniqueID = [];

// plot function
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

        // wineData.forEach(function(data){
        //   countries = JSON.parse(data.Country)
        //   console.log(countries, “parsed countries”)
        //   price = JSON.parse(data.price.replace(/\bnan\b/g, "null"))
        //   console.log(price, 'parsed price')
        //   rating = JSON.parse(data.rating.replace(/\bnan\b/g, "null"))
        //   console.log(rating, 'parsed rating')
        //   varieties = eval(‘(’+data.Variety+‘)’)})
        //   console.log(varieties, “parsed varieties”)


    

        // retrieve unique values of countries
        uniqueCountry = countryUnpack.filter((v, i, a) => a.indexOf(v) === i);
        console.log(uniqueCountry);

      
        // loop through each unique country, grab the ID and push it to an array. uniqueID was declared as global variable
        uniqueCountry.forEach(function(value, index) {
          uniqueID.push(index);
          console.log(index);
          console.log(value);
          console.log(uniqueID);
        });
        
     
        var data = [{
          type: 'parcoords',
          visible: true,
          line: {
            // color: unpack(wineData, 'country'),
            color:  Array.apply(0,new Array(43)).map(function(_,i){ return i+1 }),
            colorscale: 'Electric',
            cmin:1,
            cmax: 42,
            values: uniqueID
          },
         
          dimensions: [{
            range: [0,43],
            tickvals: uniqueID,
            ticktext: uniqueCountry,
            label: 'Countries',
            values: uniqueCountry
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
            range: [0,6],
            label: 'Variety',
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