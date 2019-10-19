function show_result() {
    var mytable =document.createElement('table');
    mytable.id = 'mytable';
    mytable.className = 'table_class';
    document.body.appendChild(mytable);
    var result = [['1','2','3'], ['2','4','4'], ['5','9','1']];
    var row=mytable.insertRow(0);
    var cell1 = row.insertCell(0);
    cell1.innerHTML = result[0];
    var cell2 = row.insertCell(1);
    cell2.innerHTML = result[1];
}

function menue_show(){
    var menue = document.getElementById('menue')
    if (menue.style.visibility=="hidden"){
        menue.style.visibility="unset"
    }
    else{
        menue.style.visibility="hidden"
    }
};

$(function(){
    $("#menue_hide").on("click",function(){
        var menue = document.getElementById('menue')
        menue.style.visibility="hidden"
    })
});