import React from "react";
import { createRoot } from "react-dom/client";
import { SWRConfig } from "swr";
import Router from "./Router";

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Failed to find the root element");
const root = createRoot(rootElement);

root.render(
  <React.StrictMode>
    <SWRConfig
      value={{
        dedupingInterval: 1000 * 10, // Dedupe every 10 seconds
        revalidateOnFocus: false, // Don't refetch when tab regains focus
        revalidateOnReconnect: false, // Don't refetch when network reconnects
        refreshInterval: 0, // Disable automatic polling
      }}
    >
      <Router />
    </SWRConfig>
  </React.StrictMode>,
);
