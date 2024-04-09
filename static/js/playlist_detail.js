function organize() {
  var dropdown1 = document.getElementById("dropdown1");
  var dropdown2 = document.getElementById("dropdown2");
  var selectedOption1 = dropdown1.options[dropdown1.selectedIndex].value;
  var selectedOption2 = dropdown2.options[dropdown2.selectedIndex].value;

  switch (selectedOption1) {
    case "releaseDateNewOld":
      if (selectedOption2 === "create") {
        executePythonFile("sorting_algorithm.py", "release_date", true, true);
      } else if (selectedOption2 === "update") {
        executePythonFile("sorting_algorithm.py", "release_date", true, false);
      }
      break;
    case "releaseDateOldNew":
      if (selectedOption2 === "create") {
        executePythonFile("sorting_algorithm.py", "release_date", false, true);
      } else if (selectedOption2 === "update") {
        executePythonFile("sorting_algorithm.py", "release_date", false, false);
      }
      break;
    case "trackNameAZ":
      if (selectedOption2 === "create") {
        executePythonFile("sorting_algorithm.py", "track_name", false, true);
      } else if (selectedOption2 === "update") {
        executePythonFile("sorting_algorithm.py", "track_name", false, false);
      }
      break;
    case "trackNameZA":
      if (selectedOption2 === "create") {
        executePythonFile("sorting_algorithm.py", "track_name", true, true);
      } else if (selectedOption2 === "update") {
        executePythonFile("sorting_algorithm.py", "track_name", true, false);
      }
      break;
    case "artistNameAZ":
      if (selectedOption2 === "create") {
        executePythonFile("sorting_algorithm.py", "artist_name", false, true);
      } else if (selectedOption2 === "update") {
        executePythonFile("sorting_algorithm.py", "artist_name", false, false);
      }
      break;
    case "artistNameZA":
      if (selectedOption2 === "create") {
        executePythonFile("sorting_algorithm.py", "artist_name", true, true);
      } else if (selectedOption2 === "update") {
        executePythonFile("sorting_algorithm.py", "artist_name", true, false);
      }
      break;
    default:
      window.location.href = "500";
  }

  var progress = document.getElementById("progress");
  progress.style.display = "block";
}

function executePythonFile(pythonFile, sortingType, isReverse, isNew) {
  var playlistId = window.location.pathname.split("/").pop();
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/execute_python", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        showCompleted();
      } else {
        window.location.href = "500";
      }
    }
  };
  var data = JSON.stringify({
    python_file: pythonFile,
    playlist_id: playlistId,
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
  }, 3000);
}
