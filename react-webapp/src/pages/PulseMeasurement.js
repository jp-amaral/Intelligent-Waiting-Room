import React from "react";
import { Link } from "react-router-dom";

import "../styles/PulseMeasurement.css";
import { Image,  StyleSheet, Text, View } from 'react-native';

import Box from '@material-ui/core/Box';


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
      
      <div className="coluna-50" >ola</div>      
      <div className="coluna-60" >olaaa</div>
     
    </div>

    
  
  );
}

export default Home;

