import React from "react";
import { render } from "react-dom";
import dotenv from "dotenv";

dotenv.config();

import App from "./App";

import "./styles/main.scss";

render(<App />, document.getElementById("root"));

const dfMessenger = document.querySelector("df-messenger");
