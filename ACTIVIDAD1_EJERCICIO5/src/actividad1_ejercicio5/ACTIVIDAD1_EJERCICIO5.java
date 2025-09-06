/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package actividad1_ejercicio5;


/**
 *
 * @author Asus
 */
import java.util.Scanner;
public class ACTIVIDAD1_EJERCICIO5 {
    public static void main(String[] args){
        double suma,x,y;

        Scanner scanner = new Scanner(System.in);

        System.out.println("Ingresa un numero para suma:");
        suma =scanner.nextDouble();
        System.out.println("Ingresa un numero para x:");
        x=scanner.nextDouble();
        System.out.println("Ingresa un numero para y:");
        y=scanner.nextDouble();

        suma=calculos.calcular_suma(suma, x);
        x=calculos.calcular_x(x, y);

        suma= suma+ (x/y);
        System.out.println("El valor de la suma es:" + suma);
 
    }
}
