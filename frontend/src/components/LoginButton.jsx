import React from 'react';
import { generateCodeVerifier, generateCodeChallenge } from '../utils/pkce';

const LoginButton = () => {
  const handleLogin = async () => {
    const codeVerifier = generateCodeVerifier();
    localStorage.setItem('pkce_code_verifier', codeVerifier);
    const codeChallenge = await generateCodeChallenge(codeVerifier);

    const params = new URLSearchParams({
      client_id: process.env.REACT_APP_KEYCLOAK_CLIENT_ID,
      redirect_uri: process.env.REACT_APP_KEYCLOAK_REDIRECT_URI,
      response_type: 'code',
      scope: 'openid profile email',
      code_challenge_method: 'S256',
      code_challenge: codeChallenge
    });

    window.location.href = `${process.env.REACT_APP_KEYCLOAK_URL}/realms/${process.env.REACT_APP_KEYCLOAK_REALM}/protocol/openid-connect/auth?${params.toString()}`;
  };

  return <button onClick={handleLogin}>Login with Keycloak</button>;
};

export default LoginButton;
