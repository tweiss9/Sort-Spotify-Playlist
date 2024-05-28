function organize() {
  var progress = document.getElementById("progress");
  progress.style.display = "block";
  var dropdown1 = document.getElementById("dropdown1");
  var dropdown2 = document.getElementById("dropdown2");
  var selectedOption1 = dropdown1.options[dropdown1.selectedIndex].value;
  var selectedOption2 = dropdown2.options[dropdown2.selectedIndex].value;

  const optionsMap = {
    releaseDateNewOld: {
      sortingType: "release_date",
      isReverse: true,
      isNew: true,
    },
    releaseDateOldNew: {
      sortingType: "release_date",
      isReverse: false,
      isNew: true,
    },
    trackNameAZ: { sortingType: "track_name", isReverse: false, isNew: true },
    trackNameZA: { sortingType: "track_name", isReverse: true, isNew: true },
    artistNameAZ: { sortingType: "artist_name", isReverse: false, isNew: true },
    artistNameZA: { sortingType: "artist_name", isReverse: true, isNew: true },
  };

  if (selectedOption1 in optionsMap) {
    const { sortingType, isReverse } = optionsMap[selectedOption1];
    const isNew = selectedOption2 === "create";

    executeSorting(sortingType, isReverse, isNew);
  } else {
    window.location.href = "500";
    progress.style.display = "none";
  }
}

async function executeSorting(sortingType, isReverse, isNew) {
  const playlistId = window.location.pathname.split("/").pop();
  const data = {
    playlist_id: playlistId,
    sorting_type: sortingType,
    is_reverse: isReverse,
    is_new: isNew,
  };

  try {
    const response = await fetch("/execute_sorting", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      console.log("Sorting completed!");
    } else {
      window.location.href = "500";
    }
  } catch (error) {
    console.error("Error:", error);
  } finally {
    showCompleted();
  }
}

function showCompleted() {
  var progress = document.getElementById("progress");
  progress.innerText = "Completed!";
  setTimeout(function () {
    progress.style.display = "none";
  }, 3000);
}
