import { createRoot } from "react-dom/client";
import App from "./App";
import { getHubSessionId } from "./lib/session";
import "./index.css";

getHubSessionId();

const root = document.getElementById("root");
if (!root) {
  throw new Error("Root element #root was not found");
}

createRoot(root).render(<App />);
