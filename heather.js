// country, price, points, variety

d3.csv("data/Wine_price_rating_variety.csv").then(function(wineData) {
    wineData.forEach(function(data) {
        console.log(wineData);
        var Countries = wineData.map(data => data.country);
        var Varieties = wineData.map(data => data.variety);
        data.price = +data.price;
        data.points = +data.points;
        console.log("Countries:", Countries);
        console.log("Price:", data.price);
        console.log("Points:", data.points);
        console.log("Varieties:", Varieties);
   
    });

});


    // log a list of names
    // var countries = wineData.map(data => data.country);
    // console.log("countries", countries);
    // wineData.forEach(function(data) {
    //     console.log("countries", countries)
    // });

    // var Price = wineData.map(data => data.price);
    // // console.log("Price", Price);
    // wineData.forEach(function(data) {
    //     console.log("Price", Price)
    // });

    // Cast each hours value in tvData as a number using the unary + operator
    // wineData.forEach(function(data) {
    //   data.price = +data.price;
    //   data.points = +data.points;
    //   console.log("Price:", data.price);
    //   console.log("Points:", data.points);
    // });

  