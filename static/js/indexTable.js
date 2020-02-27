function showRows(fromRow, windowSize, tBody, showInfo) {
    const maxRows = tBody.rows.length;
    const toRow = fromRow + windowSize;
    for(let i=fromRow; i < toRow; i++) {
      tBody.rows[i].style.display = "table-row";
    }
    for(let i=toRow; i < maxRows; i++) {
      tBody.rows[i].style.display = "none";
    }

    showInfo.innerHTML = "Showing " + fromRow + " to " + toRow + " of " + maxRows + " packages"
}


document.addEventListener("DOMContentLoaded", function (event) {

    const tBody = document.getElementById("packageTable");
    const select = document.getElementById("rowsToShow");
    const showInfo = document.getElementById("showingInfo");
    if (select !==null) {

      const windowSize = parseInt(select.value);
      const fromRow = 0;
      showRows(fromRow, windowSize, tBody, showInfo)

      select.addEventListener("change", (event) => {
        const wSize = parseInt(event.target.value);

        showRows(fromRow, wSize, tBody, showInfo)
      });

    }
});
