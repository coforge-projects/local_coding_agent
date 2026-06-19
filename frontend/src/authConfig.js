import { PublicClientApplication } from "@azure/msal-browser";

export const msalInstance = new PublicClientApplication({
  auth: {
    clientId: "3391fe42-2d9b-48ad-ade1-5844af903324",
    authority: "https://login.microsoftonline.com/b727a530-a0d5-4fb8-bd40-d8f9763e97db",
    redirectUri: "http://localhost:5173",
  },
  cache: {
    cacheLocation: "localStorage",
    storeAuthStateInCookie: false,
  },
});