(() => {
  const canvas = document.createElement('canvas');
  canvas.id = 'chain-bg';
  Object.assign(canvas.style, {
    position: 'fixed',
    inset: '0',
    width: '100%',
    height: '100%',
    zIndex: '0',
    pointerEvents: 'none',
    opacity: '0.35'
  });
  document.body.prepend(canvas);

  const ctx = canvas.getContext('2d');
  let W, H, nodes = [], mouseX = -1000, mouseY = -1000;

  const COLORS = [
    'rgba(192,132,252,',   // purple
    'rgba(244,114,182,',   // pink
    'rgba(94,234,212,',    // teal
    'rgba(167,139,250,'    // lavender
  ];

  const LINE_DIST = 160;
  const NODE_COUNT_FACTOR = 0.00004;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
    initNodes();
  }

  function initNodes() {
    const count = Math.max(25, Math.floor(W * H * NODE_COUNT_FACTOR));
    nodes = [];
    for (let i = 0; i < count; i++) {
      nodes.push(createNode());
    }
  }

  function createNode() {
    const isBlock = Math.random() > 0.6;
    return {
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.25,
      vy: (Math.random() - 0.5) * 0.2,
      size: isBlock ? 3 + Math.random() * 5 : 1.5 + Math.random() * 2,
      isBlock,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      pulse: Math.random() * Math.PI * 2,
      pulseSpeed: 0.008 + Math.random() * 0.012
    };
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      a.pulse += a.pulseSpeed;

      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < LINE_DIST) {
          const alpha = (1 - dist / LINE_DIST) * 0.35;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = a.color + alpha + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    for (const n of nodes) {
      const glow = 0.4 + Math.sin(n.pulse) * 0.2;

      if (n.isBlock) {
        const half = n.size / 2;
        ctx.beginPath();
        ctx.roundRect(n.x - half, n.y - half, n.size, n.size, 1.5);
        ctx.fillStyle = n.color + glow + ')';
        ctx.fill();
        ctx.strokeStyle = n.color + (glow * 0.6) + ')';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      } else {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.size, 0, Math.PI * 2);
        ctx.fillStyle = n.color + glow + ')';
        ctx.fill();
      }

      n.x += n.vx;
      n.y += n.vy;

      if (n.x < -20) n.x = W + 20;
      if (n.x > W + 20) n.x = -20;
      if (n.y < -20) n.y = H + 20;
      if (n.y > H + 20) n.y = -20;
    }

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw();
})();
