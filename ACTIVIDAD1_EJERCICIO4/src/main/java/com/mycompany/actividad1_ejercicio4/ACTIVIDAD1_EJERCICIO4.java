/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.actividad1_ejercicio4;

/**
 *
 * @author Asus
 */
public class ACTIVIDAD1_EJERCICIO4 {

    public static void main(String[] args) {
    double edadjuan=9;
    double edadalberto, edana, edmama;
    edadalberto= Calculos.caledad_alberto(edadjuan);
    edana=Calculos.caledad_ana(edadjuan);
    edmama=Calculos.caledad_mama(edadjuan, edana, edadalberto);
    System.out.println("Edad de Juan" + edadjuan);
    System.out.println("Edad de Ana" + edana);
    System.out.println("Edad de Alberto" + edadalberto);
    System.out.println("Edad de Mama" + edmama);
        
    }
}
