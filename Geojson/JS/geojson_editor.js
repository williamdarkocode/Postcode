const default_sub_lines = require('./Sub_Lines_var');
const fs = require('fs');



function get_line_names() {
    const names = new Set();
    const rt_sym = new Set();
    for(let line of default_sub_lines.features) {
        names.add(line.properties.name);
        rt_sym.add(line.properties.rt_symbol);
    }
}
// get_line_names();
// max_zoom: 16
// min_zoom: 10

function line_to_colour() {
    let lines_colours = {
        'G':'#d5eb89',
        'Q':'#f7d149',
        'M':'#f1b566',
        'S':'#aaadaf',
        'A':'#71b0e1',
        'B-D':'#f1b566',
        'B-D-F-M':'#f1b566',
        'R':'#f7d149',
        'N-Q-R':'#f7d149',
        'N-Q':'#f7d149',
        'N-R':'#f7d149',
        'F':'#f1b566',
        'F-M':'#f1b566',
        'E':'#71b0e1',
        '7':'#c36caa',
        'J-Z':'#ffe181',
        'L':'#b4b6b9',
        'A-C':'#71b0e1',
        'D':'#f1b566',
        '1-2-3':'#dd7170',
        'B':'#f1b566',
        '4-5-6':'#88c991',
        'N':'#f7d149',
        '1':'#dd7170',
        'N-W':'#f7d149',
        '2-3':'#dd7170',
        '2':'#dd7170',
        '4-5':'#88c991',
        '5':'#88c991',
        '4':'#88c991',
        '3':'#dd7170',
        'A-C-E':'#71b0e1',
        'N-Q-R-W':'#f7d149',
        'N-R-W':'#f7d149',
        '6':'#88c991',
        'R-W': '#f7d149'
    };

    let lines_temp = default_sub_lines;

    for(let line of lines_temp.features) {
        line.properties['strokeColor'] = lines_colours[line.properties.name];
    }

    const data = JSON.stringify(lines_temp);

    // fs.writeFile('./Sub_Lines_Edit.geojson', (err, data) => {
    //     if (err) throw err;
    //     console.log('done');
    // });
    
    fs.writeFileSync('./Sub_Lines_Edit.geojson', data);

      
}

function main() {
    line_to_colour();
}

main();