// eslint-disable-next-line strict
const fs = require('fs');
const path = require('path');
const { cesium_ion_post } = require('./cesium_request.js');

async function main() {
    const subcontent_filePath = path.join(__dirname, '../../flood/30jiami/0/subcontent.txt');
    const subcontent_str = fs.readFileSync(subcontent_filePath, 'utf8');
    const subcontent = subcontent_str.trim().split('\n').map(parseFloat);

    try {
        for (let index = 64; index < subcontent.length; index++) {
            const value = subcontent[index];
            const input = path.join(__dirname, `../../flood/30jiami/${value}/clearXYDpHrgb_0.05.las`);
            const position_dir = path.join(__dirname, `../../flood/30jiami/${value}/center_point_position_0.05.txt`);
            const position_str = fs.readFileSync(position_dir, 'utf8');
            const position = position_str.trim().split(' ').map(parseFloat);
            await cesium_ion_post(input, position, value, index);
            console.log('Array of values:', position);
            console.log(`cesium_ion_post completed for value: ${index + 1} - ${value}`);
        }
    } catch (err) {
        console.error('Error:', err);
    }
}

main();
