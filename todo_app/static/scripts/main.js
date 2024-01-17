function updateItem(checkbox){
  fetch("/update-item", {
    method: 'post',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(
      { 
        "id" : checkbox,
      }
    ),
  });
}