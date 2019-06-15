// country, price, points, variety
var url = "/api_rating";

var countries
var varieties
console.log("here")

d3.json(url).then(function(wineData) {
    console.log(wineData)
    countries = wineData.map(data => data.country);
    varieties = wineData.map(data => data.variety);
    console.log("Countries:", countries)
    console.log("Varieties:", varieties)

    wineData.forEach(function(data) {
        data.price = +data.price;
        data.points = +data.points;
        console.log("Price:", data.price)
        console.log("Points:", data.points)
    });
});