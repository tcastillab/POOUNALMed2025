/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package actividad1_ejercicio12;

import java.util.Scanner;

/**
 *
 * @author Asus
 */
public class ACTIVIDAD1_EJERCICIO12 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        double horas,valorhora,retencion,sal_bruto, salario_neto;

        Scanner scanner = new Scanner(System.in);

        System.out.println("Ingresa un numero para las horas trabajadas:");
        horas =scanner.nextDouble();
        
        System.out.println("Ingresa un numero para el valor de la hora:");
        valorhora=scanner.nextDouble();
        
        System.out.println("Ingresa un numero entero de retencion:");
        retencion=scanner.nextDouble();
        
        System.out.println("Ingresa un numero entero de retencion:");
        
        sal_bruto=cal_rete.cal_sal_bruto(horas, valorhora);
        
        double por_retencion=cal_rete.cal_por_retencion(retencion);
        
        
        double valor_rete=cal_rete.cal_retencion(por_retencion, sal_bruto);
        
        salario_neto=cal_rete.salario_neto(sal_bruto, valor_rete);
        
                
        System.out.println("El salario bruto del trabajador es:"+sal_bruto);
        System.out.println("El valor de la retencion en la fuente es:"+ valor_rete);
        System.out.println("El salario neto del trabajor es:"+ salario_neto);
        
    }
    
}
