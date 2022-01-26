const fs = require('fs');

fs.readFile('data.json', 'utf8', function (err, data) {
    if (err) throw err;
    data = JSON.parse(data);
    final = [];
    for (let key in data) {
        data[key] = data[key].split("\n")
        if (data[key].length > 1) final.push(JSON.stringify({prompt: key, completion: data[key].join("\n")}));
    }
    fs.writeFile('data.jsonl', final.join("\n"), function (err) {
        if (err) throw err;
        console.log('complete');
    })
});