/* ========== BLOG ENHANCEMENTS — SHARED JS ========== */

(function () {
  /* ---------- Back to Top ---------- */
  const backToTopBtn = document.getElementById('backToTop');
  if (backToTopBtn) {
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          if (window.scrollY > 400) {
            backToTopBtn.classList.add('visible');
          } else {
            backToTopBtn.classList.remove('visible');
          }
          ticking = false;
        });
        ticking = true;
      }
    });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Social Sharing ---------- */
  // Copy Link button
  const copyBtn = document.getElementById('shareCopyLink');
  if (copyBtn) {
    copyBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        copyBtn.classList.add('copied');
        const originalText = copyBtn.querySelector('.share-btn-text');
        if (originalText) {
          const prev = originalText.textContent;
          originalText.textContent = 'Copied!';
          setTimeout(() => {
            originalText.textContent = prev;
            copyBtn.classList.remove('copied');
          }, 2000);
        }
      }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = window.location.href;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        copyBtn.classList.add('copied');
        const originalText = copyBtn.querySelector('.share-btn-text');
        if (originalText) {
          const prev = originalText.textContent;
          originalText.textContent = 'Copied!';
          setTimeout(() => {
            originalText.textContent = prev;
            copyBtn.classList.remove('copied');
          }, 2000);
        }
      });
    });
  }

  // LinkedIn & X share buttons — populate hrefs dynamically
  const pageUrl = encodeURIComponent(window.location.href);
  const pageTitle = encodeURIComponent(document.title);

  const linkedinBtn = document.getElementById('shareLinkedIn');
  if (linkedinBtn) {
    linkedinBtn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${pageUrl}`;
  }

  const xBtn = document.getElementById('shareX');
  if (xBtn) {
    xBtn.href = `https://x.com/intent/tweet?url=${pageUrl}&text=${pageTitle}`;
  }

  /* ---------- Giscus ---------- */
  const giscusContainer = document.getElementById('giscusWidget');
  if (giscusContainer) {
    const script = document.createElement('script');
    script.src = 'https://giscus.app/client.js';
    script.setAttribute('data-repo', 'aupadh12/enigmaAI');
    script.setAttribute('data-repo-id', 'R_kgDOTponwg');
    script.setAttribute('data-category', 'Announcements');
    script.setAttribute('data-category-id', 'DIC_kwDOTponws4DEQn_');
    script.setAttribute('data-mapping', 'pathname');
    script.setAttribute('data-strict', '0');
    script.setAttribute('data-reactions-enabled', '1');
    script.setAttribute('data-emit-metadata', '0');
    script.setAttribute('data-input-position', 'bottom');
    script.setAttribute('data-theme', 'preferred_color_scheme');
    script.setAttribute('data-lang', 'en');
    script.setAttribute('data-loading', 'lazy');
    script.crossOrigin = 'anonymous';
    script.async = true;
    giscusContainer.appendChild(script);
  }
})();
