const api = "http://127.0.0.1:5000";

window.onload = () => {
    var search_button = document.getElementById("button-addon2");
    search_button.addEventListener("click",searchButtonOnClick);
    var save_button = document.getElementById("save-button");
    save_button.addEventListener("click",productFormOnSubmit);
    
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
    const table = document.getElementById("table-search-results");
    const TableBody = table.tBodies[0];
    var search_box_text_field = document.getElementById("search_text_field");
    text = search_box_text_field.value;
    const xhr = new XMLHttpRequest();
    var request_url = 'http://127.0.0.1:5000/search?name=' + text;
    xhr.open('GET', request_url);
    xhr.onload = () => {
            const jsonObject = JSON.parse(xhr.response);
            
            while (TableBody.firstChild) {
                TableBody.removeChild(TableBody.firstChild);
            }
            jsonObject.forEach((row) => {
                const tr = document.createElement("tr");
                console.log(row);
                var td = document.createElement("td");
                td.textContent = row.id;
                tr.appendChild(td);
                td = document.createElement("td");
                td.textContent = row.name;
                tr.appendChild(td);
                td = document.createElement("td");
                td.textContent = row.production_year;
                tr.appendChild(td);
                td = document.createElement("td");
                td.textContent = row.price;
                tr.appendChild(td);
                td = document.createElement("td");
                td.textContent = row.color;
                tr.appendChild(td);
                td = document.createElement("td");
                td.textContent = row.size;
                tr.appendChild(td);
                

                TableBody.appendChild(tr);
            });
       
    };
    xhr.send();
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE
    const name_text_field = document.getElementById("name");
    const production_year_text_field = document.getElementById("production");
    const price_text_field = document.getElementById("price");
    const color_text_field = document.getElementById("color");
    const size_text_field = document.getElementById("size");
    var newDocument = {
        "id": "123TRY",
        "name": name_text_field.value,
        "production_year": Number(production_year_text_field.value),
        "price": Number(price_text_field.value),
        "color": Number(color_text_field.value),
        "size": Number(size_text_field.value)

    };
    var json = JSON.stringify(newDocument);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/add-product', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
       console.log(xhr.response);
       if(xhr.status == 200){
            alert("OK");
            name_text_field.value = "";
            production_year_text_field.value = "";
            size_text_field.value = "";
            color_text_field.value= "";
            price_text_field.value = "";
       }
    };
    xhr.send(json);
    // END CODE HERE
}

