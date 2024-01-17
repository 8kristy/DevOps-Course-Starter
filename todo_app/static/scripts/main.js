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
    console.log(result)
    window.location.href = result.url
  });
}