import React, { useEffect } from 'react';

const Callback = () => {
  useEffect(() => {
    const handleCallback = async () => {
      const url = new URL(window.location.href);
      const code = url.searchParams.get('code');
      const codeVerifier = localStorage.getItem('pkce_code_verifier');

      if (!code || !codeVerifier) return;

      const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/exchange`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ code, code_verifier: codeVerifier })
      });

      if (response.ok) {
        console.log('Успешно авторизован через PKCE!');
        localStorage.removeItem('pkce_code_verifier');
      } else {
        console.error('Ошибка авторизации');
      }
    };

    handleCallback();
  }, []);

  return <div>Авторизация...</div>;
};

export default Callback;
