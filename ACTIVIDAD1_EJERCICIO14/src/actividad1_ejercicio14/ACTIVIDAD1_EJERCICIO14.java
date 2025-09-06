/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package actividad1_ejercicio14;

import java.util.Scanner;

/**
 *
 * @author Asus
 */
public class ACTIVIDAD1_EJERCICIO14 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        double numero,num_cuadrado,num_cubo;
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Ingrese un numero:");
        numero = scanner.nextDouble();
        
        num_cuadrado = calculos.cal_cuadrado(numero);
        num_cubo= calculos.cal_cubo(numero);
        
        System.out.println("EL numero al cuadrado es igual a:"+num_cuadrado);
        System.out.println("El numero al cubo es igual a:"+num_cubo);
        
        
    }
    
}
