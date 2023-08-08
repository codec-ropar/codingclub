$(window).mousemove(function (e) {
    $(".background").css(
        "background-position",
        `calc(50% + ${(window.innerWidth / 2) - e.clientX}px * -1) calc(50% + ${(window.innerHeight / 2) - e.clientY}px * -1)`
    );
});

document.addEventListener('click', function (event) {
    const canvas = document.getElementById('firecracker-canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const boundingRect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - boundingRect.left;
    const mouseY = event.clientY - boundingRect.top;

    const particleCount = 100;
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: mouseX,
            y: mouseY,
            offsetX: Math.random() * 10 - 5,
            offsetY: Math.random() * 10 - 5,
            radius: Math.random() * 3 + 1,
            color: `hsl(${Math.random() * 360}, 100%, 50%)`,
            speedX: Math.random() * 6 - 3,
            speedY: Math.random() * 6 - 3,
            opacity: 1,
        });
    }

    const explosions = [];
    explosions.push(particles);

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        explosions.forEach((explosion, explosionIndex) => {
            explosion.forEach((particle, index) => {
                particle.x += particle.speedX;
                particle.y += particle.speedY;
                particle.opacity -= 0.02;

                ctx.globalAlpha = particle.opacity;
                ctx.beginPath();
                ctx.arc(
                    particle.x + particle.offsetX,
                    particle.y + particle.offsetY,
                    particle.radius,
                    0,
                    Math.PI * 2
                );
                ctx.fillStyle = particle.color;
                ctx.fill();
                ctx.closePath();

                if (particle.opacity <= 0) {
                    explosion.splice(index, 1);
                }
            });

            if (explosion.length === 0) {
                explosions.splice(explosionIndex, 1);
            }
        });

        if (explosions.length > 0) {
            requestAnimationFrame(animate);
        }
    }

    animate();
});
