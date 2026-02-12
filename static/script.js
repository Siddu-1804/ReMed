// Front-end form handler — posts JSON to the configured NGROK endpoint
(function () {
  const NGROK_URL = 'https://clarine-unaffected-maynard.ngrok-free.dev/register';

  const form = document.getElementById('registerForm');
  const message = document.getElementById('formMessage');
  const toast = document.getElementById('toast');

  if (!form) return;

  function showToast(text, type = 'success', timeout = 4500) {
    if (!toast) return;
    toast.textContent = '';
    toast.className = 'toast show ' + (type === 'error' ? 'error' : 'success');

    const icon = document.createElement('span');
    icon.className = 'icon';
    icon.innerHTML = type === 'error' ? '✖' : '✓';
    const msg = document.createElement('div');
    msg.style.flex = '1';
    msg.style.paddingLeft = '6px';
    msg.textContent = text;

    toast.appendChild(icon);
    toast.appendChild(msg);

    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.className = 'toast';
      toast.innerHTML = '';
    }, timeout);
  }

  function setInlineMessage(text, ok = true) {
    if (!message) return;
    message.textContent = text;
    message.style.color = ok ? '#064E3B' : '#7f1d1d';
  }

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }

    setInlineMessage('Sending…', true);

    const name = (document.getElementById('name') || {}).value || '';
    const phone = (document.getElementById('phone') || {}).value || '';
    if (!name.trim() || !phone.trim()) {
      setInlineMessage('Please enter both name and phone number.', false);
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Request Access'; }
      showToast('Please provide name and phone number.', 'error');
      return;
    }

    const normalizedPhone = phone.trim();

    // We send only JSON to the NGROK endpoint; file uploads are optional and not posted here.
    const payload = {
      name: name.trim(),
      phoneNumber: normalizedPhone,
      phone_number: normalizedPhone
    };

    // No file upload is sent from the front-end

    try {
      const res = await fetch(NGROK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const text = await res.text().catch(() => res.statusText);
        setInlineMessage('Server error: ' + text, false);
        showToast('Unable to send registration: ' + (text || res.status), 'error');
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Request Access'; }
        return;
      }

      let json = null;
      try { json = await res.json(); } catch (e) { /* ignore */ }

      const successText = (json && json.message) ? json.message : 'We received your request.';
      // Show the requested confirmation to the user
      const smsNotice = 'Check your sms for webhook link';
      setInlineMessage(smsNotice, true);
      showToast(smsNotice);
      form.reset();
    } catch (err) {
      setInlineMessage('Network error: ' + (err.message || err), false);
      showToast('Network error — please try again.', 'error');
    } finally {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Request Access'; }
    }
  });
})();
