
function setTime(t) {
    document.getElementById('time').innerHTML = t;
}

function setLocal(row, col, state) {
    let e = document.querySelector(`#Row-${row} > .${col}.Seat`);
    if (e) {
        if (state) {
            e.style.fill = 'white';
            e.style.stroke = 'black';
        } else {
            e.style.fill = 'transparent';
            e.style.stroke = '';
        }
    }
}

function setRemote(row, col, color) {
    let e = document.querySelector(`#Row-${row} > .${col}.Desk`);
    if (e) {
      e.style.fill = color;
    }
}

Color = function(hexOrObject) {
    var obj;
    if (hexOrObject instanceof Object) {
        obj = hexOrObject;
    } else {
        obj = LinearColorInterpolator.convertHexToRgb(hexOrObject);
    }
    this.r = obj.r;
    this.g = obj.g;
    this.b = obj.b;
}
Color.prototype.asRgbCss = function() {
    return "rgb("+this.r+", "+this.g+", "+this.b+")";
}

var LinearColorInterpolator = {
    convertHexToRgb: function(hex) {
        match = hex.replace(/#/,'').match(/.{1,2}/g);
        return new Color({
            r: parseInt(match[0], 16),
            g: parseInt(match[1], 16),
            b: parseInt(match[2], 16)
        });
    },

    findColorBetween: function(left, right, percentage) {
        newColor = {};
        components = ["r", "g", "b"];
        for (var i = 0; i < components.length; i++) {
            c = components[i];
            newColor[c] = Math.round(left[c] + (right[c] - left[c]) * percentage / 100);
        }
        return new Color(newColor);
    }
}

let colors = [];
let base = [new Color('#ffffff'), new Color('#ffdea6'), new Color('#fdbd4d'), new Color('#f7943e'), new Color('#f15a38')]
for (let i = 0; i < 30; i++) {
    if (i >= 20) {
        colors.push(base[4].asRgbCss());
    } else {
        let a = base[Math.floor(i / 5)];
        let b = base[Math.floor((i+5) / 5)];
        let p = (i - 5*Math.floor(i/5))/5;

        colors.push(LinearColorInterpolator.findColorBetween(a,b,p).asRgbCss());
    }
}

document.querySelector('#Header use').style.fill = 'white';

let i = 0;

const options = {weekday: 'short', month: 'short', day: '2-digit', hour:'2-digit', minute: '2-digit'};

// TODO: Too tired to fix
let e = document.querySelector(`#Row-10 > .H.Seat`);
e.style.fill = 'transparent';
e.style.stroke = 'transparent';
e = document.querySelector(`#Row-10 > .H.Desk`);
e.style.fill = colors[0];

let f = () => {
    let s = new Date(data[i][0]*1000).toLocaleString('en-US', options).replace(',', '');
    setTime(s);
    for (let j = 0; j < data[i][1].length; j++) {
        let v = data[i][1][j];
        let row = v[0];
        let col = v[1];
        setLocal(row, col, v[2] != 0);
        setRemote(row, col, colors[v[3]]);
    }
    i++;
};

f();
setInterval(f, 100);