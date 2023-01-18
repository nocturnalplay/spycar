import Head from "next/head";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const [body, setbody] = useState(0);
  const ws = useRef();
  const [websoc, setwebsoc] = useState("connecting...");
  const [socdata, setsocdata] = useState({
    acspeed: 0,
    acdirection: "",
    rodirection: "",
    rospeed: 0,
  });

  const conectWebSocket = () => {
    ws.current = new WebSocket(`${process.env.WS}`);
    ws.current.onopen = (e) => {
      ws.current.send("2828");
      setwebsoc("connected");
    };
    ws.current.onmessage = (e) => {
      let data = JSON.parse(e.data);
      setsocdata(() => data);
    };
  };

  const gesture = () => {
    setTimeout(() => {
      setbody(1);
      conectWebSocket();
    }, 1500);
    const getbu = document.getElementById("getbutton");
    const gettit = document.getElementsByClassName("home-tit");
    for (let i = 0; i < gettit.length; i++) {
      gettit[i].style.animation = "offtitle 0.7s 0.5s ease-in-out forwards";
      gettit[i].style.opacity = 1;
      gettit[i].style.transform = "translate(0,-50px)";
    }
    getbu.style.animation = "offbutton 0.5s 0.1s ease-in-out forwards";
    getbu.style.opacity = 1;
    getbu.style.transform = "translate(0,-50px)";
  };
  console.log(socdata);
  return (
    <>
      <Head>
        <title>Car-Gesture</title>
      </Head>
      {body == 0 && (
        <div className="car-conteiner">
          <h1 className="home-tit">gesture electronices</h1>
          <p className="home-tit">
            controle the car through the hand gesture using digital image
            processing
          </p>
          <button id="getbutton" onClick={gesture}>
            get started
          </button>
        </div>
      )}
      {body == 1 && (
        <div className="car-stream">
          <div className="websoc-connect">{websoc}</div>
          <div className="websoc-rpm">
            <h4>rpm</h4>
            <span>{socdata.acspeed}</span>
          </div>
          <div className="websoc-dd">
            <div className="websoc-dir">
              <h4>moving direction:</h4>
              <span>{socdata.acdirection}</span>
              <span>{socdata.rodirection}</span>
            </div>
            <div className="websoc-deg">
              {socdata.rospeed
                ? Math.abs(((socdata.rospeed - 0) * 60) / (0 - 100))
                : 0}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
