document.addEventListener("DOMContentLoaded", () => {
    const explanationBox = document.querySelector(".map-feedback");
    const regionDots = document.querySelectorAll(".dot");
    const correctRegion = document.body.dataset.correctRegion; // injected from template
    const explanations = JSON.parse(document.getElementById("explanations-json").textContent);
  
    regionDots.forEach(dot => {
      dot.addEventListener("click", () => {
        const selectedRegion = dot.dataset.region;
        const idx = document.body.dataset.idx; // you'll add this below
        window.location.href = `/final_quiz/question/${idx}?selected_region=${selectedRegion}`;
  
        // Highlight selected
        regionDots.forEach(d => d.classList.remove("selected"));
        dot.classList.add("selected");
  
        // Get and display feedback
        const explanation = explanations[selectedRegion] || "No explanation available.";
        const isCorrect = selectedRegion === correctRegion;
  
        explanationBox.className = "map-feedback " + (isCorrect ? "correct" : "incorrect");
        explanationBox.textContent = explanation;
        explanationBox.style.display = "block";
      });
    });
  });  