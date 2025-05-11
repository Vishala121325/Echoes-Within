const capsuleList = document.getElementById('capsule-list');
const audioInput = document.getElementById('audioInput');
const audioPreview = document.getElementById('audioPreview');

audioInput.addEventListener('change', function() {
    audioPreview.innerHTML = '';
    Array.from(audioInput.files).forEach(file => {
        if (file.type.startsWith('audio/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.classList.add('preview-item');
                div.innerHTML = `<audio controls><source src="${e.target.result}" type="${file.type}">Your browser does not support the audio element.</audio>`;
                audioPreview.appendChild(div);
            };
            reader.readAsDataURL(file);
        }
    });
});

function renderCapsules(capsules) {
    capsuleList.innerHTML = '';
    const now = new Date();

    capsules.forEach(capsule => {
        const capsuleDiv = document.createElement('div');
        capsuleDiv.classList.add('capsule');

        if (now >= new Date(capsule.unlockDate)) {
            capsuleDiv.classList.add('open');
            let mediaHTML = '';

            if (capsule.photos) {
                capsule.photos.forEach(photo => {
                    mediaHTML += `<img src="/uploads/${photo}" width="200"><br>`;
                    mediaHTML += `<a href="/uploads/${photo}" download>Download Photo</a><br>`;
                });
            }

            if (capsule.videos) {
                capsule.videos.forEach(video => {
                    mediaHTML += `<video src="/uploads/${video}" width="250" controls></video><br>`;
                    mediaHTML += `<a href="/uploads/${video}" download>Download Video</a><br>`;
                });
            }

            capsuleDiv.innerHTML = `
                <p><strong>Unlocked!</strong></p>
                <p>${capsule.message}</p>
                ${mediaHTML}
            `;

        } else {
            capsuleDiv.classList.add('locked');
            const timeLeft = Math.max(0, new Date(capsule.unlockDate) - now);
            capsuleDiv.innerHTML = `
                <p><strong>Locked</strong></p>
                <p>Opens in: ${formatCountdown(timeLeft)}</p>
            `;
        }

        capsuleList.appendChild(capsuleDiv);
    });
}


function updateCountdowns() {
    const countdowns = document.querySelectorAll('.countdown');
    countdowns.forEach(c => {
        const unlockTime = new Date(c.dataset.unlock).getTime();
        const now = new Date().getTime();
        const distance = unlockTime - now;

        if (distance < 0) {
            if (!c.classList.contains('unlocked')) {
                c.innerHTML = "Ready!";
                c.closest('.capsule-card').classList.add('fade-unlock');
                c.classList.add('unlocked'); // prevent re-animating every 60s
            }
        } else {
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            c.innerHTML = `${days}d ${hours}h ${minutes}m`;
        }
    });
}

setInterval(updateCountdowns, 60000); // update every 60 seconds
updateCountdowns(); // initial call
