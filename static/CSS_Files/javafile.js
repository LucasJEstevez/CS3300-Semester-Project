/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction(dropdownid)
{
  document.getElementById(dropdownid).classList.toggle("show");
}

function filterFunction(dropdownid, inputid)
{
  const input = document.getElementById(inputid);
  const filter = input.value.toUpperCase();
  const div = document.getElementById(dropdownid);
  const a = div.getElementsByTagName("a");
  for (let i = 0; i < a.length; i++)
  {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1)
    {
      a[i].style.display = "";
    }
    else
    {
      a[i].style.display = "none";
    }
  }
}

function filterTable() {
const makeInput = document.getElementById("modelInput").value.toUpperCase();
const yearInput = document.getElementById("yearInput").value.toUpperCase();
const rows = document.querySelectorAll("#csvTable tbody tr");

rows.forEach(row =>
{
  const make = row.cells[1].textContent.toUpperCase();
  const year = row.cells[0].textContent.toUpperCase();

  // Check if row matches the filter
  const makeMatch = make.indexOf(makeInput) > -1;
  const yearMatch = year.indexOf(yearInput) > -1;

  if (makeMatch && yearMatch)
  {
      row.style.display = "";
  }
  else
  {
      row.style.display = "none";
  }
});
}

// Call `filterTable` on keyup events for filtering inputs
document.getElementById("modelInput").addEventListener('keyup', filterTable);
document.getElementById("yearInput").addEventListener('keyup', filterTable);

function toggleUserDropdown()
{
  var dropdown = document.getElementById("userDropdown");
  if (dropdown.style.display === "none" || dropdown.style.display === "")
  {
    dropdown.style.display = "block";
  }
  else
  {
    dropdown.style.display = "none";
  }
}