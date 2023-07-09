function organize() {
  var dropdown1 = document.getElementById("dropdown1");
  var dropdown2 = document.getElementById("dropdown2");
  var selectedOption1 = dropdown1.options[dropdown1.selectedIndex].value;
  var selectedOption2 = dropdown2.options[dropdown2.selectedIndex].value;

  if (selectedOption1 === "releaseDateNewOld" && selectedOption2 === "create") {
    executePythonFile("sorting_algorithm.py", "release_date", true, true);
  } else if (
    selectedOption1 === "releaseDateNewOld" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("sorting_algorithm.py", "release_date", true, false);
  } else if (
    selectedOption1 === "releaseDateOldNew" &&
    selectedOption2 === "create"
  ) {
    executePythonFile("sorting_algorithm.py", "release_date", false, true);
  } else if (
    selectedOption1 === "releaseDateOldNew" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("sorting_algorithm.py", "release_date", false, false);
  } else if (
    selectedOption1 === "trackNameAZ" &&
    selectedOption2 === "create"
  ) {
    executePythonFile("sorting_algorithm.py", "track_name", false, true);
  } else if (
    selectedOption1 === "trackNameAZ" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("sorting_algorithm.py", "track_name", false, false);
  } else if (
    selectedOption1 === "trackNameZA" &&
    selectedOption2 === "create"
  ) {
    executePythonFile("sorting_algorithm.py", "track_name", true, true);
  } else if (
    selectedOption1 === "trackNameZA" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("sorting_algorithm.py", "track_name", true, false);
  } else if (
    selectedOption1 === "artistNameAZ" &&
    selectedOption2 === "create"
  ) {
    executePythonFile("sorting_algorithm.py", "artist_name", false, true);
  } else if (
    selectedOption1 === "artistNameAZ" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("sorting_algorithm.py", "artist_name", false, false);
  } else if (
    selectedOption1 === "artistNameZA" &&
    selectedOption2 === "create"
  ) {
    executePythonFile("sorting_algorithm.py", "artist_name", true, true);
  } else if (
    selectedOption1 === "artistNameZA" &&
    selectedOption2 === "update"
  ) {
    executePythonFile("sorting_algorithm.py", "artist_name", true, false);
  } else {
    window.location.href = "/error.html";
  }

  var progress = document.getElementById("progress");
  progress.style.display = "block";
}

function executePythonFile(pythonFile, sortingType, isReverse, isNew) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/execute_python", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        showCompleted();
      } else {
        showErrorMessage();
      }
    }
  };
  var data = JSON.stringify({
    python_file: pythonFile,
    sorting_type: sortingType,
    is_reverse: isReverse,
    is_new: isNew,
  });
  xhr.send(data);
}
function showCompleted() {
  var progress = document.getElementById("progress");
  progress.innerText = "Completed!";
  setTimeout(function () {
    progress.style.display = "none";
  }, 5000);
}
function showErrorMessage() {
  var progress = document.getElementById("progress");
  progress.innerText = "Error";
  setTimeout(function () {
    progress.style.display = "none";
  }, 5000);
}