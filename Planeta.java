/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.actividad2_ejercicio_2_2;

/**
 *
 * @author Asus
 */
public class Planeta {
    String nombre=null;
    int cantidadSatelites =0;
    double masa =0;
    double volumen =0;
    int diametro=0;
    int distanciaSol=0;
    tipoplaneta tipo;
    boolean esObservable=false;
    
Planeta(String nombre,int cantidadSatelites,double masa,double volumen,int diametro,int distanciaSol,tipoplaneta tipo,boolean esObservable ){
    this.nombre=nombre;
    this.cantidadSatelites=cantidadSatelites;
    this.masa=masa;
    this.volumen=volumen;
    this.diametro=diametro;
    this.distanciaSol=distanciaSol;
    this.tipo=tipo;
    this.esObservable=esObservable;

     }
void imprimir(){
    System.out.println("Nombre del planeta=" + nombre);
    System.out.println("Cantidad del satelite ="+ cantidadSatelites);
   
    System.out.println("Masa del planeta ="+masa);
    System.out.println("Volumen del planeta="+volumen);
    System.out.println("Diametro del planeta="+diametro);
    System.out.println("Distancia al Sol="+distanciaSol);
    System.out.println("Es observable="+esObservable);    
    }
double calcularDensidad(){
    return masa/volumen;
           
    }
boolean esPlanetaExterior(){
    float limite=(float) (149597870*3.4);
    if  (distanciaSol >limite){
        return true;        
    }
    else{
        return false;
    }
    }
}
