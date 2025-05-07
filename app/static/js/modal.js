document.addEventListener("DOMContentLoaded", () => {
  // JavaScript to fetch insights
  document.querySelectorAll(".insights-button").forEach(button => {
    button.addEventListener("click", async () => {
      const resumeId = button.getAttribute("data-resume-id");
      const insightsDiv = document.getElementById(`insights-${resumeId}`);

      if (!insightsDiv.classList.contains("hidden")) {
        insightsDiv.classList.add("hidden");
        return;
      }

      insightsDiv.classList.remove("hidden");
      insightsDiv.innerHTML = "Loading...";

      try {
        const response = await fetch(`/insights/${resumeId}`);
        const data = await response.text();

        if (response.ok) {
          insightsDiv.innerHTML = data;
        } else {
          insightsDiv.innerHTML = "Error loading insights.";
        }
      } catch (error) {
        console.error("Fetch error:", error);
        insightsDiv.innerHTML = "Error loading insights.";
      }
    });
  });

  // JavaScript to handle the modal for cleaning job descriptions
  const cleanBtn = document.getElementById("cleanJdBtn");

  if (cleanBtn) {
    cleanBtn.addEventListener("click", async () => {
      const textarea = document.querySelector("textarea[name='job_description']");
      const jobDescription = textarea.value;

      if (!jobDescription.trim()) {
        alert("Please paste a job description before cleaning.");
        return;
      }

      try {
        const response = await fetch("/clean-jd", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ job_description: jobDescription })
        });

        const data = await response.json();

        if (response.ok) {
          const structuredContent = document.getElementById("structuredContent");
          const structuredView = document.getElementById("structuredView");

          structuredContent.innerHTML = "";

          // Build cleaned JD text to update textarea
          let cleanedJdText = "";
          for (const [section, content] of Object.entries(data.cleaned_sections)) {
            structuredContent.innerHTML += `
              <div class="mb-2">
                <strong>${section}</strong>
                <p class="ml-2 text-sm text-gray-700 whitespace-pre-wrap">${content || "Not found"}</p>
              </div>
            `;
            cleanedJdText += `${section}:\n${content || "Not found"}\n\n`;
          }

          // Update textarea with cleaned JD
          textarea.value = cleanedJdText.trim();

          structuredView.style.display = "block";
        } else {
          alert("Something went wrong while cleaning the JD.");
        }
      } catch (error) {
        console.error("Cleaning failed:", error);
        alert("Error communicating with server.");
      }
    });
  }
});