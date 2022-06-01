import React from "react";
import { Link } from "react-router-dom";
import BannerImage from "../assets/room.jpeg";
import "../styles/Home.css";
import { Image,  StyleSheet, Text, View } from 'react-native';

import Box from '@material-ui/core/Box';
import { AllInbox, CenterFocusStrong } from "@material-ui/icons";

const Contador = () => {
  
  return (
    <Box
      style={{
        backgroundColor: '#333',
      
        borderRadius: 10,
        color: '#eee',
        display: "flex",
        float:'right',
        minHeight: 200,
        padding: 12,
        marginRight: 130,
        marginTop:50,
        width: 300,
   
      }}
    >
      Contagem de pessoas
    </Box>
  );
}

function Home() {
  return (
    <div className="linha" style={{backgroundcolor: "black"}}>
      
       <div className="coluna-50" >
        <Image source={BannerImage} style={{ width: 1300, height: 755, borderRadius: 10}}/>
      </div>      
      <div className="coluna-60" ><Contador></Contador></div>
     
    </div>

    
  
  );
}

export default Home;

