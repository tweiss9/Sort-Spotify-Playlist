function showProgress() {
  var dropdown1 = document.getElementById("dropdown1");
  var dropdown2 = document.getElementById("dropdown2");
  var selectedOption1 = dropdown1.options[dropdown1.selectedIndex].value;
  var selectedOption2 = dropdown2.options[dropdown2.selectedIndex].value;

  if (selectedOption1 === "releaseDateNewOld" && selectedOption2 === "create") {
    executePythonFile("releaseDate.py", true, true);
  } else if (
    selectedOption1 === "releaseDateOldNew" &&
    selectedOption2 === "create"
  ) {
    executePythonFile("releaseDate.py", false, true);
  } else if (
    selectedOption1 === "releaseDateNewOld" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("releaseDate.py", true, false);
  } else if (
    selectedOption1 === "releaseDateOldNew" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("releaseDate.py", false, false);
  } else {
    console.log("Default action");
  }

  var progress = document.getElementById("progress");
  progress.style.display = "block";
  setTimeout(function () {
    progress.style.display = "none";
  }, 3000);
}

function executePythonFile(pythonFile, isReverse, isNew) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/execute_python", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        console.log(xhr.responseText);
      } else {
        console.error("An error occurred while executing the Python file.");
      }
    }
  };
  var data = JSON.stringify({ python_file: pythonFile, is_reverse: isReverse, is_new: isNew });
  xhr.send(data);
}
