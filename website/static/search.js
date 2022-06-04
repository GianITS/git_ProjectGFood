const numIng = document.getElementById('NumIng');
const ingLTwo = document.querySelector('.ing.LTwo');
const ingTwo = document.querySelector('.ing.Two');
const ingLThree = document.querySelector('.ing.LThree');
const ingThree = document.querySelector('.ing.Three');

numIng.onchange = function() {
    numIngValue = numIng.value;
    if (numIngValue == "1") {
        ingLTwo.classList.remove('ingShow');
        ingTwo.classList.remove('ingShow');
        ingLThree.classList.remove('ingShow');
        ingThree.classList.remove('ingShow');
    }
    else if (numIngValue == "2") {
        ingLTwo.classList.add('ingShow');
        ingTwo.classList.add('ingShow');
        ingLThree.classList.remove('ingShow');
        ingThree.classList.remove('ingShow');
    }
    else if (numIngValue == "3") {
        ingLTwo.classList.add('ingShow');
        ingTwo.classList.add('ingShow');
        ingLThree.classList.add('ingShow');
        ingThree.classList.add('ingShow');
    }
}