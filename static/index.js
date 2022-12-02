function delRow(id) {
    fetch("/delrow", {
        method: 'POST',
        body: JSON.stringify({row_id: id}),
    
    }).then((_res) => {
        window.location.href = "/";
    });
    
}
 