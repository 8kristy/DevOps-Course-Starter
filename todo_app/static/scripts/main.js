function updateItem(checkbox){
  fetch("/update-item", {
    method: 'post',
    redirect: 'follow',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(
      { 
        "id" : checkbox,
      }
    ),
  })
  .then(result => {
    window.location.href = result.url
  });
}

function removeItem(id){
  fetch("/remove-item", {
    method: 'post',
    redirect: 'follow',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(
      { 
        "id" : id,
      }
    ),
  })
  .then(result => {
    window.location.href = result.url
  });
}