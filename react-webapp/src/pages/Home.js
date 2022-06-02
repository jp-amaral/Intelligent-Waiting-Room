import React from "react";
import { Link } from "react-router-dom";
import BannerImage from "../assets/room.jpeg";
import "../styles/Home.css";
import { Image,  StyleSheet, Text, View } from 'react-native';

import Box from '@material-ui/core/Box';
import { AllInbox, CenterFocusStrong } from "@material-ui/icons";


function Home() {
  return (
    <div className="linha">
      <img className="room" src={BannerImage} />
      <div className="rect">
        <h1 className="npd">Nº of people detected</h1>
      </div>
      <div className="rect2">
        <h1 className="pdr">People detected in the room</h1>
      </div>
      <div className="rect3">
      </div>
    </div>

    
  
  );
}

export default Home;

