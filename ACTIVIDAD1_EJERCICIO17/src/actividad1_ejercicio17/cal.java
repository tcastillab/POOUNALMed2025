/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package actividad1_ejercicio17;

/**
 *
 * @author Asus
 */
public class cal {
    static double calcular_longitud_circulo(double radio){
        double long_cir=2*Math.PI*radio;
        return long_cir;
    }
    static double calcular_area_circulo(double radio){
        double area_circulo =Math.PI*Math.pow(radio, 2);
        return area_circulo;
    }
}
