document.addEventListener('DOMContentLoaded', function() {
  const submitBtn = document.getElementById('submit');
  const loader = document.getElementById('loader');
  const answerDiv = document.getElementById('answer');
  
  submitBtn.addEventListener('click', function() {
    const question = document.getElementById('question').value.trim();
    
    if (!question) {
      answerDiv.innerText = "Please enter a question";
      return;
    }
    
    // Show loader and disable button
    loader.style.display = 'block';
    submitBtn.disabled = true;
    answerDiv.innerText = '';
    
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      const url = tabs[0].url;
      
      // Extract video ID from YouTube URL
      const videoId = new URL(url).searchParams.get('v');
      if (!videoId) {
        answerDiv.innerText = "Not a valid YouTube video page";
        loader.style.display = 'none';
        submitBtn.disabled = false;
        return;
      }

      // Send question and video_id to your Python backend
      fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_id: videoId, question: question }),
      })
        .then((response) => response.json())
        .then((data) => {
          answerDiv.innerText = data.answer || data.error || "No answer available";
        })
        .catch((error) => {
          answerDiv.innerText = "Error connecting to server";
          console.error(error);
        })
        .finally(() => {
          // Hide loader and enable button regardless of success/failure
          loader.style.display = 'none';
          submitBtn.disabled = false;
        });
    });
  });
});