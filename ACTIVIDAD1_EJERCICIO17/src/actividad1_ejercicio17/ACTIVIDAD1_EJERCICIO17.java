/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package actividad1_ejercicio17;
import java.util.Scanner;
/**
 *
 * @author Asus
 */
public class ACTIVIDAD1_EJERCICIO17 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
       Scanner scanner =new Scanner(System.in);
       double area_cir,longitud_cir,radio;
       System.out.println("Ingrese un numero para el radio de la circunferencia:");
       radio=scanner.nextDouble();
       
       longitud_cir=cal.calcular_longitud_circulo(radio);
       area_cir=cal.calcular_area_circulo(radio);
       
       System.out.println("La longitud de la circunferencia es igual a:"+longitud_cir);
       System.out.println("EL área del circulo es igual a:"+area_cir);
       
 
        
    }
    
}
