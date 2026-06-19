import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

import { PublicClientApplication } from "@azure/msal-browser";
import { MsalProvider } from "@azure/msal-react";

// ✅ Correct MSAL config
const msalInstance = new PublicClientApplication({
  auth: {
    clientId: "3391fe42-2d9b-48ad-ade1-5844af903324",
    authority: "https://login.microsoftonline.com/b727a530-a0d5-4fb8-bd40-d8f9763e97db", // ✅ use common for now
    redirectUri: window.location.origin,
  },
});

// ✅ CRITICAL: initialize BEFORE render
msalInstance.initialize().then(() => {
  ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
      <MsalProvider instance={msalInstance}>
        <App />
      </MsalProvider>
    </React.StrictMode>
  );
});
``