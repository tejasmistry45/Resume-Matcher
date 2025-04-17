// modal.js

// Show modal with resume details when "View" button is clicked
document.querySelectorAll('.view-button').forEach(button => {
    button.addEventListener('click', function() {
        const resumeId = this.getAttribute('data-id');
        fetch(`/resume-details/${resumeId}`)
            .then(response => response.json())
            .then(data => {
                // Show the modal
                const modal = document.getElementById('resume-modal');
                const resumeDetails = document.getElementById('resume-details');

                resumeDetails.innerHTML = `
                    <h4 class="font-semibold">Skills Matched: ${data.skills_matched}</h4>
                    <p><strong>Tools: </strong>${data.tools}</p>
                    <p><strong>Experience: </strong>${data.experience} years</p>
                    <p><strong>Score: </strong>${data.score}</p>
                `;

                modal.style.display = 'flex';
            });
    });
});

// Close the modal
document.getElementById('close-modal').addEventListener('click', function() {
    document.getElementById('resume-modal').style.display = 'none';
});
