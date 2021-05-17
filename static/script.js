if (document.getElementById('total_hit')){
    $.getJSON("static/hit.json", 
        function(json) {
        document.getElementById('total_hit').innerHTML = `TOTAL HIT ${json.total}`;
    });
}